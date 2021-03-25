from flask import Blueprint, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
from os import urandom
import codecs

def verify_params(params, logger) -> bool:
    valid_len = 1024
    num_keys = 2
    valid_photons = [[1, 0], [0, 1], [0.707, -0.707], [0.707, 0.707]]
    valid_base = ['+', 'x']

    try:
        assert len(params.keys()) == num_keys
        assert isinstance(params['photons'], list)
        assert isinstance(params['basis'], list)
        assert len(params['basis']) == valid_len
        assert len(params['photons']) == valid_len
        for i in range(valid_len):
            assert params['photons'][i] in valid_photons
            assert params['basis'][i] in valid_base
        return True
    except Exception as e:
        logger.exception(str(e))
        return False

key_distribution_blueprint = Blueprint('key_distribution', __name__)
key_distribution_blueprint.config = {}

@key_distribution_blueprint.record
def record_params(setup_state):
    key_distribution_blueprint.config = setup_state.app.config

@key_distribution_blueprint.route('/flag', methods=['GET'])
def distribute():
    logger = key_distribution_blueprint.config['logger']

    try:
        if request.method == 'GET':

            params = request.get_json()
            if not verify_params(params, logger):
                return 'invalid parameters', 422

            for k in params.keys():
                if params[k] == [params[k][0]] * len(params[k]):
                    return 'parameters are not random enough', 422

            params['photons'] = [complex(real, imag) for real, imag in params['photons']]
            params['key_size'] = 256

            BB84 = key_distribution_blueprint.config['BB84']
            BB84.initialize(params)
            basis, e_basis, key = BB84.distribute(True)
            e_basis = ''.join(e_basis)

            flag = key_distribution_blueprint.config['flag']
            flag = pad(flag.encode(), AES.block_size)
            flag = AES.new(key, AES.MODE_ECB).encrypt(flag)
            flag = b64encode(flag).decode()

            image_url = key_distribution_blueprint.config['image_url']
            image_url = codecs.encode(image_url, 'rot-13')
            image_url = ''.join(ch for ch in image_url if ch.isalnum())

            response = jsonify({'basis': basis, 'flag': flag})
            response.set_cookie(image_url)
            response.headers["Server"] = 'none of your business'

            x_forwarded_for = request.headers.getlist("X-Forwarded-For")
            if x_forwarded_for:
                client = x_forwarded_for[0]
            else:
                client = request.remote_addr
            is_local = client in ['localhost', '127.0.0.1']

            if request.headers.getlist("I-See-What-You-Did-There"):

                if is_local:

                    db = key_distribution_blueprint.config['db']
                    icecream = urandom(32).hex()
                    while not db.save(icecream, e_basis):
                        icecream = urandom(32).hex()

                    ssh_password = key_distribution_blueprint.config['ssh_password']
                    ssh_port = key_distribution_blueprint.config['ssh_port']
                    response.headers["Eavesdropper-Bounced-But-Dropped-His-Icecream"] = icecream
                    response.headers[f"Eavesdropper-Bounced-But-Dropped-His-Keys-For-Port-{ssh_port}"] = ssh_password

                else:
                    response.headers["You-Saw-Nothing"] = "only localhost is the all-seer"
            return response, 200
        else:
            return 'method not implemented', 501
    except Exception as e:
        logger.exception(str(e))
        return 'an unexpected error occurred', 500
