
/* Ensures that our toolchain definitions work. */
#ifndef PYMAKE_SAMPLE
#error PYMAKE_SAMPLE undefined
#endif

#include <iostream>


int main(int argc, char *argv[])
{
    std::cout << "Using toolchain: " << PYMAKE_TOOLCHAIN << '\n';
    return 0;
}
