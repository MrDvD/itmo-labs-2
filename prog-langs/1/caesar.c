#include<stdio.h>
#include<stdlib.h>

void encrypt(char * word, int shift) {
  if (shift < 0) {
    shift = 26 + shift % 26;
  }
  for (int i = 0; word[i] != '\0'; i++) {
    char c = word[i];
    if (c >= 'a' && c <= 'z') {
      char new = 'a' + (c - 'a' + shift) % 26;
      if (new < 'a') {
        word[i] = 'z' - ('a' - new - 1);
      } else if (new > 'z') {
        word[i] = 'a' + (new - 'z' - 1);
      } else {
        word[i] = new;
      }
    }
    if (c >= 'A' && c <= 'Z') {
      char new = 'A' + (c - 'A' + shift) % 26;
      if (new < 'A') {
        word[i] = 'Z' - ('A' - new - 1);
      } else if (new > 'z') {
        word[i] = 'A' + (new - 'Z' - 1);
      } else {
        word[i] = new;
      }
    }
  }
  printf("Your encoded message: %s\n", word);
}

void decrypt(char * word, int shift) {
  if (shift < 0) {
    shift = 26 + shift % 26;
  }
  for (int i = 0; word[i] != '\0'; i++) {
    char c = word[i];
    if (c >= 'a' && c <= 'z') {
      char new = c - shift % 26;
      if (new < 'a') {
        word[i] = 'z' - ('a' - new - 1);
      } else if (new > 'z') {
        word[i] = 'a' + (new - 'z' - 1);
      } else {
        word[i] = new;
      }
    }
    if (c >= 'A' && c <= 'Z') {
      char new = c - shift % 26;
      if (new < 'A') {
        word[i] = 'Z' - ('A' - new - 1);
      } else if (new > 'Z') {
        word[i] = 'A' + (new - 'Z' - 1);
      } else {
        word[i] = new;
      }
    }
  }
  printf("Your decoded message: %s\n", word);
}

int main(int argc, char **argv) {
  if (argc != 3) {
    printf("Incorrect usage\n");
    return 1;
  }
  char * word = argv[1];
  int N = atoi(argv[2]);
  encrypt(word, N);
  decrypt(word, N);
  return 0;
}