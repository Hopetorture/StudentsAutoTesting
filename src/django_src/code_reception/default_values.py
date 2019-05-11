CPP_TEMPLATE = '''
#include <iostream>

using namespace std;

int main ()
{
    cout << "Hello world!!!";    
    return 0;
}'''

SUPPORTED_TOOLSETS = [
    {'name': 'c++98', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++98'},
    {'name': 'c++14', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++14'},
]