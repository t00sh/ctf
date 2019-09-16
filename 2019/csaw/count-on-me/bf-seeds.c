#include <stdlib.h>
#include <stdio.h>
#include "mersenne-twister.h"

/*
 * git clone https://github.com/cslarsen/mersenne-twister.git
 * cd mersenne-twister
 * git checkout c0bdd01d23594d7a95894d17b3264a26847c3a3e
 * git patch < mersenne-twister.patch
 */
int main(int argc, char **argv) {
    unsigned long i = atol(argv[1]);
    uint32_t a, b, c;
    int ok1 = 0, ok2 = 0;

    while (!ok1 || !ok2) {
        seed(i);

        a = rand_u32();
        b = rand_u32();
        c = rand_u32();
        if (a == b) {
            ok1 = 1;
            printf("a=%x, b=%x, c=%x, seed=%x\n", a, b, c, i);
        } else if (a == c || b == c) {
            ok2 = 1;
            printf("a=%x, b=%x, c=%x, seed=%x\n", a, b, c, i);
        }
        i++;
    }
    return 0;
}
