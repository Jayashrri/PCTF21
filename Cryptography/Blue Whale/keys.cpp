#include <iostream>
#include <vector>
#include <string>
using namespace std;

vector<uint8_t> Xor(vector<uint8_t>& message, vector<uint8_t>& key) {
    size_t n = message.size();
    vector<uint8_t> cipher(n, 0);
    for (size_t i=0; i<n; i++)
        cipher.at(i) = message.at(i) ^ key.at(i%n);
    return cipher;
}

vector<uint8_t> bytes_fromhex(string& hex) {
    size_t n = hex.length()/2;
    vector<uint8_t> bytes(n, 0);
    for (size_t i=0; i<n; i++)
        bytes.at(i) = stoul(hex.substr(i*2, 2), nullptr, 16);
    return bytes;
}

string bytes_tostr(vector<uint8_t>& bytes) {
    string str;
    str.reserve(bytes.size());
    for (uint8_t byte: bytes)
        str.push_back(byte);
    return str;
}

int main() {  
    string key;
    cout << "password is needed to get the keys. wrong password might result in wrong keys.\n";  
    cout << "enter password: ";
    getline(cin, key);

    try {
        string cipher("f705128fc7f1e021d8bb7af84d49caf583b8332c45185689da96f02985037ae2f9aab39867caf2e74ad16d3da66f4d0a7d819d");
        vector<uint8_t> cipher_bytes = bytes_fromhex(cipher);
        vector<uint8_t> key_bytes = bytes_fromhex(key);
        vector<uint8_t> decrypted_bytes = Xor(cipher_bytes, key_bytes);
        cout << bytes_tostr(decrypted_bytes) << endl;
    }
    catch (...) {
        cout << "incorrect password\n";
    }

    return 0;
}
