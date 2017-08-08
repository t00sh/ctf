/* gcc -O2 -Wall gen_password.c -o gen_password */
/* Generate combinaisons of passwords from a given charset */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#define CHARSET_MAJ "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define CHARSET_MIN "abcdefghijklmnopqrstuvwxyz"
#define CHARSET_DIG "0123456789"
#define CHARSET_SPE "&~\"#'{([-|`_\\^@])=}+/?,;.:!<>"

struct charset {
  const char *charset;
  int positions[256];
  int len;
};

/*
 * Build the table for optimization.
 * We can then, from a given charset letter,
 * know its position in O(1).
 */
void build_charset(struct charset *charset_table, const char *charset) {
  int i;

  memset(charset_table, 0, sizeof(*charset_table));
  charset_table->len = strlen(charset);

  for(i = 0; i < charset_table->len; i++) {
    charset_table->positions[(unsigned char)charset[i]] = i;
  }

  charset_table->charset = charset;
}

int password_next(struct charset *charset, char *pwd, int pwd_len) {
  const char *charset_str;
  int charset_len;
  int *charset_positions;
  int i;

  charset_str = charset->charset;
  charset_len = charset->len;
  charset_positions = charset->positions;

  i = pwd_len - 1;

  while(pwd[i] == charset_str[charset_len - 1] && i >= 0) {
    pwd[i] = charset_str[0];
    i--;
  }

  if(i < 0)
    return 0;

  pwd[i] = charset_str[charset_positions[(unsigned char)pwd[i]] + 1];

  return 1;
}

void gen_from_charset(FILE *stream, struct charset *charset, int len) {
  char *password;
  int i;

  if((password = malloc(len + 1)) == NULL) {
    perror("[-] Failed to alloc memory: ");
    exit(EXIT_FAILURE);
  }

  for(i = 0; i < len; i++) {
    password[i] = charset->charset[0];
  }
  password[len] = 0;

  do {
    fprintf(stream, "%s\n", password);
  } while(password_next(charset, password, len));

  free(password);
}


int main(int argc, char **argv) {
  const char *charset_str = CHARSET_MAJ CHARSET_MIN CHARSET_DIG CHARSET_SPE;
  struct charset charset;

  if(argc != 2 && argc != 3) {
    printf("Usage : %s <len> [<charset>]\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  if(argc == 3) {
    charset_str = argv[2];
  }

  build_charset(&charset, charset_str);

  gen_from_charset(stdout, &charset, atoi(argv[1]));

  return 0;
}
