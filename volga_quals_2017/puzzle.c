#include <openssl/sha.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define X_SIZE 29
#define X_KNOWN_BYTES 24

static unsigned char sha1_last_bits[] = "\x03\xff\xff\xff";


void rand_bytes(unsigned char *x, int n) {
  const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  int i;

  for(i = 0; i < n; i++) {
    x[i] = charset[rand() % (sizeof(charset) - 1)];
  }
}

int check_sha1(unsigned char *sha1) {
  int i, offset;

  offset = SHA_DIGEST_LENGTH - sizeof(sha1_last_bits) + 1;

  for(i = 0; i < sizeof(sha1_last_bits) - 1; i++) {
    if((sha1[i + offset] & sha1_last_bits[i]) !=
       sha1_last_bits[i])
      return 0;
  }

  return 1;
}

int main(int argc, char **argv) {
  unsigned char x[X_SIZE + 1];
  unsigned char sha[SHA_DIGEST_LENGTH];
  int i;

  srand(time(NULL));

  if(argc != 2) {
    printf("Usage : %s <x>\n");
    exit(EXIT_FAILURE);
  }

  if(strlen(argv[1]) != X_KNOWN_BYTES) {
    printf("x need to be %d bytes long !\n", X_KNOWN_BYTES);
    exit(EXIT_FAILURE);
  }

  memcpy(x, argv[1], X_KNOWN_BYTES);

  do {
    rand_bytes(x + X_KNOWN_BYTES, X_SIZE - X_KNOWN_BYTES);
    SHA1(x, X_SIZE, sha);

  }while(!check_sha1(sha));

  x[X_SIZE] = 0;
  printf("%s", (char*)x);

  return 0;
}
