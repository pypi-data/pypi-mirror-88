
#include <iostream>
#include <fstream>
#include "nlohmann/json.hpp"

int main(int argc, char const* argv[])
{
    std::cerr << "Converting." << std::endl;
    std::ifstream  plain_json(argv[1], std::ios::in);
    std::ofstream  ubjson(argv[2], std::ios::binary);
    nlohmann::json plain_meta_data;
    plain_json >> plain_meta_data;
    std::vector<uint8_t> bin_meta_data = nlohmann::json::to_ubjson(plain_meta_data);
    for (auto& byte : bin_meta_data)
        ubjson << byte;
    std::cerr << "Finished." << std::endl;
}
