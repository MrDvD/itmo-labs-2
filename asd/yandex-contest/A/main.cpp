#include <iostream>

struct segment {
  int l;
  int r;
};

int main() {
  int N;
  std::cin >> N;
  struct {
    short occur = 0;
    long item = -1;
  } history;
  segment ans = {0, 0};
  segment curr = {0, 0};
  for (int i = 0; i < N; i++) {
    long a;
    std::cin >> a;
    if (history.item != a) {
      history.item = a;
      history.occur = 1;
    } else {
      history.occur++;
    }
    if (history.occur == 3) {
      if (ans.r - ans.l < curr.r - curr.l) {
        ans = curr;
      }
      history.occur--;
      curr.l = i - 1;
    }
    curr.r = i;
  }
  if (ans.r - ans.l < curr.r - curr.l) {
    ans = curr;
  }
  std::cout << ans.l + 1 << " " << ans.r + 1;
  return 0;
}