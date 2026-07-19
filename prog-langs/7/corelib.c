#include <stdbool.h>
#include <stdio.h>

typedef struct Point {
  int X;
  int Y;
} Point;

int filter(Point dots[], int length, bool (*f)(Point), Point result[]) {
  int j = 0;
  for (int i = 0; i < length; i++) {
    Point dot = dots[i];
    printf("Process point in C: (%d, %d)\n", dot.X, dot.Y);
    if (f(dot)) {
      result[j++] = dot;
    }
  }
  return j;
}