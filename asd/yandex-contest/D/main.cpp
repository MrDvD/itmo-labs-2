#include <iostream>

int main() {
  int a, b, c, d;
  long long k;
  std::cin >> a >> b >> c >> d >> k;
  if (c == a * (b - 1)) {
    std::cout << a;
    return 0;
  }
  long x = a;
  for (int i = 0; i < (d < k ? d : k); i++) {
    x *= b;
    if (x < c) {
      x = 0;
      break;
    }
    x -= c;
    if (x >= d) {
      x = d;
      break;
    }
  }
  std::cout << x;
  return 0;
}