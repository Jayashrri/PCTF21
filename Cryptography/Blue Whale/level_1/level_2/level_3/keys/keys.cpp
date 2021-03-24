#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <stdexcept>
#include <exception>
#include "headers/HTTPRequest.hpp"
#include "headers/JSON.hpp"

class Decrypt {
    private:
        std::vector<uint8_t> XOR(const std::vector<uint8_t>& message, const std::vector<uint8_t>& key) {
            size_t m = message.size();
            size_t n = key.size();
            std::vector<uint8_t> cipher(m, 0);
            for (size_t i=0; i<m; i++)
                cipher.at(i) = message.at(i) ^ key.at(i%n);
            return cipher;
        }

        std::vector<uint8_t> bytes_fromhex(const std::string& hex) {
            size_t n = hex.length()/2;
            std::vector<uint8_t> bytes(n, 0);
            for (size_t i=0; i<n; i++)
                bytes.at(i) = std::stoul(hex.substr(i*2, 2), nullptr, 16);
            return bytes;
        }

        std::string bytes_tostr(const std::vector<uint8_t>& bytes) {
            std::string str;
            str.reserve(bytes.size());
            for (uint8_t byte: bytes)
                str.push_back(byte);
            return str;
        }

    public:
        std::string operator() (const std::string& cipher, const std::string& key) {
            try {
                std::vector<uint8_t> cipher_bytes = this->bytes_fromhex(cipher);
                std::vector<uint8_t> key_bytes = this->bytes_fromhex(key);
                std::vector<uint8_t> plaintext_bytes = this->XOR(cipher_bytes, key_bytes);
                return this->bytes_tostr(plaintext_bytes);
            }
            catch (const std::exception& e) {
                throw std::logic_error("incorrect password");
            }
        }
};

class Ciphertext {
    private:
        std::string request_endpoint(const std::string& filename) {
            std::ifstream file(filename, std::ios::in);
            nlohmann::json config = nlohmann::json::parse(file);
            file.close();
            std::stringstream endpoint;
            endpoint << "http://" << config["host"].get<std::string>() << ":";
            endpoint << config["port"].get<std::string>() << "/encrypted_keys";
            return endpoint.str();
        }

        std::string make_http_request(const std::string& endpoint) {
            http::Request request(endpoint);
            http::Response response = request.send("GET");
            if (response.status != 200)
                throw std::logic_error("an unexpected error occured");
            return std::string(response.body.begin(), response.body.end());
        }

    public:
        std::string operator() (const std::string& filename) {
            try {
                std::string endpoint = this->request_endpoint(filename);
                return this->make_http_request(endpoint);
            }
            catch (const std::exception& e) {
                throw std::logic_error("an unexpected error occured");
            }
        }
};

int main() {
    try {
        Ciphertext request_ciphertext;
        std::string filename = std::string(std::getenv("HOME")) + "/keys_config.json";
        std::string cipher = request_ciphertext(filename);

        std::cout << "password is needed to get the keys. wrong password might result in wrong keys." << std::endl;
        std::cout << "enter password: ";
        std::string key;
        std::getline(std::cin, key);

        Decrypt decrypt;
        std::cout << decrypt(cipher, key) << std::endl;
    }
    catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
