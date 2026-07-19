#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
 
typedef struct {
  int x;
  int y;
} Point;
 
typedef enum {
  Circle,
  Square,
  Triangle
} ShapeType;
 
typedef struct {
  Point p;
  char* name;
  ShapeType type;
} Shape;
 
typedef struct {
  Shape* shapes;
  int size;
} Container;
 
Container* create_container() {
  Container* ct = malloc(sizeof(Container));
  if (ct != NULL) {
    ct->size = 0;
    ct->shapes = NULL;
  }
  return ct;
}

Point* create_point(int x, int y) {
  Point* p = malloc(sizeof(Point));
  if (p == NULL) {
    return NULL;
  }
  p->x = x;
  p->y = y;
  return p;
}


int add_new_shape(Container* ct, char* name, Point point, ShapeType type) {
  Shape* shapes = realloc(ct->shapes, sizeof(Shape) * (ct->size + 1));
  if (shapes == NULL) {
    return -1;
  }
  Shape* new_shape = (Shape*) malloc(sizeof(Shape));
  if (new_shape == NULL) {
    free(shapes);
    return -1;
  }
  new_shape->name = name;
  new_shape->p = point;
  new_shape->type = type;
  shapes[ct->size] = *new_shape;
  free(new_shape);
  ct->shapes = shapes;
  ct->size += 1;
  return 0;
}

int remove_shape_by_index(Container* ct, int idx) {
  if (idx < 0 || ct->size - 1 < idx || ct->size == 0) {
    return -1;
  }
  Shape* shapes = malloc(sizeof(Shape) * ct->size - 1);
  if (shapes == NULL) {
    return - 1;
  } 
  for (int i = 0; i < ct->size; i++) {
    if (i == idx) {
      continue;
    } else if (i > idx) {
      shapes[i - 1] = ct->shapes[i];
    } else {
      shapes[i] = ct->shapes[i];
    }
  }
  free(ct->shapes);
  ct->shapes = shapes;
  ct->size -= 1;
  return 0;
}

void print_p(Point p) {
  printf("Point: %d, %d\n", p.x, p.y);
}

char * type_to_string(ShapeType type) {
  switch (type)
  {
  case Circle:
    return "круг";
  case Square:
    return "квадрат";
  case Triangle:
    return "треугольник";
  default:
    return "";
  }
}

void print_s(Shape shape) {
  print_p(shape.p);
  printf("Shape name: %s\n", shape.name);
  printf("Shape type: %s\n", type_to_string(shape.type));
}

void print(Container* ct) {
  printf("Size of container: %d\n", ct->size);
  printf("Container items:\n");
  for (int i = 0; i < ct->size; i++) {
    print_s(ct->shapes[i]);
    printf("- - -\n");
  }
}

void free_container(Container* ct) {
  free(ct->shapes);
  free(ct);
}
 
int main() {
  Container* container = create_container();
  if (container != NULL) {
    Point* p1 = create_point(1, 2);
    Point* p2 = create_point(5, 4);
    Point* p3 = create_point(3, 3);
    add_new_shape(container, "квадратик", *p1, Square);
    add_new_shape(container, "треугольничек", *p2, Triangle);
    print(container);
    remove_shape_by_index(container, 0);
    add_new_shape(container, "кружок", *p3, Circle);
    print(container);
    free(p1);
    free(p2);
    free(p3);
    free_container(container);
    container= NULL;

    add_new_shape(container, "кружок", *p3, Circle);
  }
}