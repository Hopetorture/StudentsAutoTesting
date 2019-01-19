#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
    int summ = 0;
    for(int i = 1; i < argc; i++){
        summ += atoi(argv[i]);
     }
    cout << summ;
    return 0;
}