#include <boost/json/parse.hpp>
#include <iostream>

int main()
{
    auto jv = boost::json::parse("[1,2,3]");
    std::cerr << jv << '\n';
    return 0;
}