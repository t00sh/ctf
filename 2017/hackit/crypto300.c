#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>

#define KEY_LENGTH 8
#define BLOCK_LENGTH 8

void f(uint8_t block[BLOCK_LENGTH], uint8_t **matrix) {
  uint8_t b1, b2;
  int b1_x, b1_y, b2_x, b2_y;
  int i, x, y, tmp;

  for(i = 0; i < BLOCK_LENGTH; i += 2) {
    b1 = block[i];
    b2 = block[i+1];
    b1_x = b1_y = 0;
    b2_x = b2_y = 0;

    for(y = 0; y < 16; y++) {
      for(x = 0; x < 16; x++) {
        if(matrix[y][x] == b1) {
          b1_x = x;
          b1_y = y;
        } else if(matrix[y][x] == b2) {
          b2_x = x;
          b2_y = y;
        }
      }
    }

    if(b1_x != b2_x || b1_y != b2_y) {
      if(b1_x == b2_x) {
        b1_y++;
        b2_y++;
        b1_y %= 16;
        b2_y %= 16;
      } else if(b1_y == b2_y) {
        b1_x++;
        b2_x++;
        b1_x %= 16;
        b2_x %= 16;
      } else {
        tmp = b1_x;
        b1_x = b2_x;
        b2_x = tmp;
      }
    }

    block[i] = matrix[b1_y][b1_x];
    block[i+1] = matrix[b2_y][b2_x];
  }
}

void f_rev(uint8_t block[BLOCK_LENGTH], uint8_t **matrix) {
  uint8_t b1, b2;
  int b1_x, b1_y, b2_x, b2_y;
  int i, x, y, tmp;

  for(i = 0; i < BLOCK_LENGTH; i += 2) {
    b1 = block[i];
    b2 = block[i+1];
    b1_x = b1_y = 0;
    b2_x = b2_y = 0;

    for(y = 0; y < 16; y++) {
      for(x = 0; x < 16; x++) {
        if(matrix[y][x] == b1) {
          b1_x = x;
          b1_y = y;
        } else if(matrix[y][x] == b2) {
          b2_x = x;
          b2_y = y;
        }
      }
    }

    if(b1_x != b2_x || b1_y != b2_y) {
      if(b1_x == b2_x) {
        b1_y--;
        b2_y--;
        if(b1_y < 0) b1_y = 15;
        if(b2_y < 0) b2_y = 15;
      } else if(b1_y == b2_y) {
        b1_x--;
        b2_x--;
        if(b1_x < 0) b1_x = 15;
        if(b2_x < 0) b2_x = 15;
      } else {
        tmp = b1_x;
        b1_x = b2_x;
        b2_x = tmp;
      }
    }

    block[i] = matrix[b1_y][b1_x];
    block[i+1] = matrix[b2_y][b2_x];
  }
}


uint8_t** matrix_generator(uint8_t secretkey[KEY_LENGTH]) {
  char *uniqKw, *expandedKey;
  int i, j, counter, uniqKwLength, expandedKeyLength;
  uint8_t **matrix;

  uniqKw = malloc(KEY_LENGTH);

  for(i = 0, uniqKwLength = 0; i < 8; i++) {
    if(memchr(uniqKw, secretkey[i], uniqKwLength) == NULL) {
      uniqKw[uniqKwLength++] = secretkey[i];
    }
  }

  expandedKey = malloc(256);
  memcpy(expandedKey, uniqKw, uniqKwLength);
  expandedKeyLength = uniqKwLength;

  for(i = 0; i < 256; i++) {
    if(memchr(uniqKw, i, uniqKwLength) == NULL) {
      expandedKey[expandedKeyLength++] = i;
    }
  }

  matrix = malloc(16 * sizeof(*matrix));
  for(i = 0; i < 16; i++)
    matrix[i] = malloc(16 * sizeof(**matrix));


  counter = 0;

  for(i = 0; i < 16; i++) {
    for(j = 0; j < 16; j++) {
      matrix[i][j] = expandedKey[counter++];
    }
  }

  return matrix;
}


void matrix_free(uint8_t **matrix) {
  int i;

  for(i = 0; i < 16; i++)
    free(matrix[i]);
  free(matrix);
}

void xor(uint8_t *r, const uint8_t *a, const uint8_t *b, int length) {
  int i;

  for(i = 0; i < length; i++) {
    r[i] = a[i] ^ b[i];
  }
}

void encrypt(const uint8_t *plain, uint8_t *cipher, int length, uint8_t key[KEY_LENGTH], uint8_t iv[BLOCK_LENGTH]) {
  uint8_t **matrix;
  int i;

  /*
   * MODE :
   * C1 = F(P1 ^ IV)
   * C2 = F(P1 ^ P2 ^ C1)
   * Ci = F(Pi-1 ^ Pi ^ Ci-1)
   */
  assert(length % BLOCK_LENGTH == 0);

  matrix = matrix_generator(key);

  xor(cipher, plain, iv, BLOCK_LENGTH);
  f(cipher, matrix);

  for(i = BLOCK_LENGTH; i < length; i += BLOCK_LENGTH) {
    xor(cipher+i, plain+(i-BLOCK_LENGTH), cipher+(i-BLOCK_LENGTH), BLOCK_LENGTH);
    xor(cipher+i, plain+i, cipher+i, BLOCK_LENGTH);
    f(cipher+i, matrix);
  }

  matrix_free(matrix);
}

void decrypt(uint8_t *plain, const uint8_t *cipher, int length, uint8_t key[KEY_LENGTH], uint8_t iv[BLOCK_LENGTH]) {
  uint8_t **matrix;
  int i;

  /*
   * MODE :
   * P1 = F_rev(C1) ^ IV
   * P2 = F_rev(C2) ^ P1 ^ C1
   * Pi = F_rev(Ci) ^ Pi-1 ^ Ci-1
   */
  assert(length % BLOCK_LENGTH == 0);

  matrix = matrix_generator(key);

  memcpy(plain, cipher, BLOCK_LENGTH);
  f_rev(plain, matrix);
  xor(plain, plain, iv, BLOCK_LENGTH);

  for(i = BLOCK_LENGTH; i < length; i += BLOCK_LENGTH) {
    memcpy(plain+i, cipher+i, BLOCK_LENGTH);
    f_rev(plain+i, matrix);
    xor(plain+i, plain+i, plain+(i-BLOCK_LENGTH), BLOCK_LENGTH);
    xor(plain+i, plain+i, cipher+(i-BLOCK_LENGTH), BLOCK_LENGTH);
  }

  matrix_free(matrix);
}


uint8_t cipher[80] = {
  0xff, 0xc2, 0xcc, 0xd6, 0x93, 0xc5, 0x96, 0xf7, 0x9c, 0x9a, 0xc3, 0x88, 0xd3, 0xca, 0x9e, 0xe6,
  0xc8, 0xc9, 0xd9, 0x82, 0xd9, 0x8f, 0xf3, 0x88, 0xd2, 0x94, 0x8a, 0xcd, 0x9c, 0xc8, 0xea, 0x7e,
  0xd3, 0xd6, 0xc7, 0xd9, 0xd2, 0xdc, 0xf0, 0x84, 0xf0, 0xc8, 0xc6, 0xc9, 0xcd, 0x93, 0xe8, 0x8a,
  0xff, 0xc0, 0xbf, 0xc5, 0xc6, 0x91, 0xda, 0xc9, 0xc7, 0xe9, 0x92, 0xda, 0xe6, 0x7e, 0xaa, 0x99,
  0xc0, 0xd2, 0xb8, 0xcd, 0xdf, 0x81, 0xeb, 0xc4, 0xda, 0xd4, 0xb4, 0xde, 0x8b, 0x97, 0xa6, 0xb0,
};

uint8_t iv[8] = {0xa5, 0xa6, 0xa7, 0xa8, 0xb5, 0xb6, 0xb7, 0xb8};


int main(void) {
  uint64_t seed, month, day, hour, min, sec;
  uint8_t key[8];
  uint8_t plain[80];
  int i;

  for(month = 4; month <= 5; month++) {
    for(day = 0; day <= 31; day++) {
      for(hour = 0; hour <= 24; hour++) {
        for(min = 0; min <= 60; min++) {
          for(sec = 0; sec <= 60; sec++) {
            seed = (2017-1970) * 100000000000ULL;
            seed += month * 1000000000ULL;
            seed += hour * 100000ULL;
            seed += min * 1000ULL;
            seed += sec;

            key[0] = seed >> 56;
            key[1] = seed >> 48;
            key[2] = seed >> 40;
            key[3] = seed >> 32;
            key[4] = seed >> 24;
            key[5] = seed >> 16;
            key[6] = seed >> 8;
            key[7] = seed >> 0;

            decrypt(plain, cipher, 80, key, iv);

            for(i = 0; i < 80; i++) {
              printf("%c", (char)plain[i]);
            }
            printf("\n");
          }
        }
      }
    }
  }

  return 0;
}
