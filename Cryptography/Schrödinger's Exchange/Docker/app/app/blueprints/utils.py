from flask import Blueprint, request, jsonify
from base64 import b64encode

def verify_photons(photons, logger) -> bool:
    valid_len = 1024
    valid_photons = [[1, 0], [0, 1], [0.707, -0.707], [0.707, 0.707]]
    
    try:
        assert isinstance(photons, list)
        assert len(photons) == valid_len
        for i in range(valid_len):
            assert photons[i] in valid_photons
        return True
    except Exception as e:
        logger.exception(str(e))
        return False

def verify_basis(basis, logger) -> bool:
    valid_len = 1024
    valid_base = ['+', 'x']

    try:
        assert isinstance(basis, list)
        assert len(basis) == valid_len
        for i in range(valid_len):
            assert basis[i] in valid_base
        return True
    except Exception as e:
        logger.exception(str(e))
        return False

def verify_bits(bits, logger) -> bool:
    valid_len = 1024
    valid_bits = ['0', '1', '\x00']

    try:
        assert isinstance(bits, list)
        assert len(bits) == valid_len
        for i in range(valid_len):
            assert bits[i] in valid_bits
        return True
    except Exception as e:
        logger.exception(str(e))
        return False

utils_blueprint = Blueprint('utils', __name__)
utils_blueprint.config = {}

@utils_blueprint.record
def record_params(setup_state):
    utils_blueprint.config = setup_state.app.config

@utils_blueprint.route('/polarize', methods=['GET'])
def polarize():
    logger = utils_blueprint.config['logger']

    try:
        if request.method == 'GET':

            params = request.get_json()
            try:
                bits = params['bits']
                basis = params['basis']
            except Exception as e:
                logger.exception(str(e))
                return 'invalid parameters', 422

            if not verify_bits(bits, logger):
                return 'invalid parameters', 422
            if not verify_basis(basis, logger):
                return 'invalid parameters', 422

            BB84 = utils_blueprint.config['BB84']
            photons = BB84.polarize_photons(bits, basis)

            _photons = []
            for photon in photons:
                real = photon.real
                real = real if real % 1 else int(real)
                imag = photon.imag
                imag = imag if imag % 1 else int(imag)
                _photons.append([real, imag])

            response = jsonify({'photons': _photons})
            response.headers["Server"] = 'none of your business'
            return response, 200
        else:
            return 'method not implemented', 501
    except Exception as e:
        logger.exception(str(e))
        return 'an unexpected error occurred', 500


@utils_blueprint.route('/measure', methods=['GET'])
def measure():
    logger = utils_blueprint.config['logger']

    try:
        if request.method == 'GET':

            params = request.get_json()
            try:
                photons = params['photons']
                basis = params['basis']
            except Exception as e:
                logger.exception(str(e))
                return 'invalid parameters', 422

            if not verify_photons(photons, logger):
                return 'invalid parameters', 422
            if not verify_basis(basis, logger):
                return 'invalid parameters', 422

            photons = [complex(real, imag) for real, imag in photons]
            BB84 = utils_blueprint.config['BB84']
            bits = BB84.measure_photons(photons, basis)

            response = jsonify({'bits': bits})
            response.headers["Server"] = 'none of your business'
            return response, 200
        else:
            return 'method not implemented', 501
    except Exception as e:
        logger.exception(str(e))
        return 'an unexpected error occurred', 500

@utils_blueprint.route('/sharedkey', methods=['GET'])
def shared_key():
    logger = utils_blueprint.config['logger']

    try:
        if request.method == 'GET':

            params = request.get_json()
            try:
                bits = params['bits']
                basis_1 = params['basis_1']
                basis_2 = params['basis_2']
            except Exception as e:
                logger.exception(str(e))
                return 'invalid parameters', 422

            if not verify_bits(bits, logger):
                return 'invalid parameters', 422
            if not verify_basis(basis_1, logger):
                return 'invalid parameters', 422
            if not verify_basis(basis_2, logger):
                return 'invalid parameters', 422

            BB84 = utils_blueprint.config['BB84']
            key = BB84.shared_key(bits, basis_1, basis_2, 256)
            key = b64encode(key).decode()

            response = jsonify({'key': key})
            response.headers["Server"] = 'none of your business'
            return response, 200
        else:
            return 'method not implemented', 501
    except Exception as e:
        logger.exception(str(e))
        return 'an unexpected error occurred', 500
