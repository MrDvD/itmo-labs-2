#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef struct Point {
   int x;
   int y;
} Point;

double process_points(Point p1, Point p2)  {
  // printf("Point recevied x: %d, y: %d\n", p1.x, p1.y);
  // printf("Point recevied x: %d, y: %d\n", p2.x, p2.y);
  return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
}

void process_point_arrays(Point array[][2], int size, double* result) {
  //printf("result: %f\n", result[i]);
  for (int i = 0; i < size; i++) {
    result[i] = process_points(array[i][0], array[i][1]);
    // printf("result: %f\n", result[i]);
  }
}