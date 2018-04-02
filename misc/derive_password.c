/* gcc -O2 -Wall derive_password.c -o derive_password */
/* Derive a password from a given one (use min/maj combinaisons + l33t) */

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>


int digit_swap(int c) {
  if(c == 'a')
    return '4';
  if(c == 'e')
    return '3';
  if(c == 't')
    return '7';
  if(c == 'l')
    return '1';
  if(c == 's')
    return '5';
  if(c == 'o')
    return '0';
  return c;
}

int digit_swap_rev(int c) {
  if(c == '4')
    return 'a';
  if(c == '3')
    return 'e';
  if(c == '7')
    return 't';
  if(c == '1')
    return 'l';
  if(c == '5')
    return 's';
  if(c == '0')
    return 'o';
  return c;
}

int next_password_digit(char *pwd, int len) {
  int i, c;

  i = len - 1;

  while(i >= 0) {
    c = digit_swap(pwd[i]);
    if(c == pwd[i] && digit_swap_rev(c) != c)
      break;

    pwd[i] = digit_swap(pwd[i]);
    i--;
  }

  if(i < 0)
    return 0;

  pwd[i] = digit_swap_rev(pwd[i]);

  return 1;
}

void derive_password_digit(FILE *stream, char *pwd, int len) {
  char *pwd_copy;
  int i;

  if((pwd_copy = strdup(pwd)) == NULL) {
    perror("[-] Failed to allocate memory:");
    exit(EXIT_FAILURE);
  }

  for(i = 0; i < len; i++) {
    pwd_copy[i] = digit_swap(pwd_copy[i]);
  }

  do {
    fprintf(stream, "%s\n", pwd_copy);
  } while(next_password_digit(pwd_copy, len));

  free(pwd_copy);
}

int next_password_maj(char *pwd, int len) {
  int i;

  i = len - 1;

  while(i >= 0) {
    if(isalpha(pwd[i])) {
      if(islower(pwd[i])) {
        break;
      } else {
        pwd[i] = tolower(pwd[i]);
      }
    }
    i--;
  }

  if(i < 0)
    return 0;

  pwd[i] = toupper(pwd[i]);

  return 1;
}

void derive_password_maj(FILE *stream, char *pwd, int len) {
  int i;

  for(i = 0; i < len; i++) {
    if(isalpha(pwd[i])) {
      pwd[i] = tolower(pwd[i]);
    }
  }

  do {
    derive_password_digit(stream, pwd, len);
  } while(next_password_maj(pwd, len));

}

int main(int argc, char **argv) {
  char *pwd;

  if(argc != 2) {
    printf("Usage : %s <password>\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  if((pwd = strdup(argv[1])) == NULL) {
    perror("[-] Failed to allocate memory\n");
    exit(EXIT_FAILURE);
  }

  derive_password_maj(stdout, pwd, strlen(pwd));

  free(pwd);

  return 0;
}
