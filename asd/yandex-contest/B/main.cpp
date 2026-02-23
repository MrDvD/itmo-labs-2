#include <iostream>
#include <stack>
#include <vector>

struct item {
  char value;
  bool isTrap;
  int idx;
};

int main() {
  std::string zoo;
  std::cin >> zoo;
  int N = zoo.length();
  std::stack<item> stack;
  std::vector<int> order;
  for (int i = 0; i < N; i++) {
    order.push_back(-1);
  }
  int animal_idx = 1, trap_idx = 1;
  for (int i = 0; i < N; i++) {
    bool isTrap = (char)std::tolower(zoo[i]) != zoo[i];
    int idx = isTrap ? trap_idx++ : animal_idx++;
    item curr = {(char)std::tolower(zoo[i]), isTrap, idx};
    if (stack.size() == 0 || stack.top().value != curr.value || stack.top().isTrap == curr.isTrap) {
      stack.push(curr);
      continue;
    }
    item top = stack.top();
    stack.pop();
    if (top.isTrap) {
      order[top.idx - 1] = curr.idx;
    } else {
      order[curr.idx - 1] = top.idx;
    }
  }
  if (stack.size() > 0) {
    std::cout << "Impossible";
    return 0;
  }
  std::cout << "Possible" << std::endl;
  for (int i = 0; i < N; i++) {
    if (order[i] != -1) {
      std::cout << order[i] << " ";
    }
  }
  return 0;
}