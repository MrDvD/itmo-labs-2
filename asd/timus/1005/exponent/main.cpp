#include <bitset>
#include <iostream>
#include <vector>

template <std::size_t N>
void fill_options(std::vector<std::bitset<N>>& options) {
  std::vector<std::bitset<N>> new_options;
  for (std::bitset<N>& o : options) {
    new_options.push_back(o << 1 | std::bitset<20>{1});
    new_options.push_back(o << 1);
  }
  options = std::move(new_options);
}

int main() {
  int N;
  std::cin >> N;
  std::vector<int> arr;
  for (int i = 0; i < N; i++) {
    int item;
    std::cin >> item;
    arr.push_back(item);
  }
  std::vector<std::bitset<20>> opts = {0, 1};
  for (int i = 0; i < N - 1; i++) {
    fill_options<20>(opts);
  }
  long ans = 2000000;
  for (std::bitset<20> o : opts) {
    long sum1 = 0, sum2 = 0, curr;
    for (int i = 0; i < N; i++) {
      if ((o >> i & std::bitset<20>{1}).test(0)) {
        sum1 += arr[i];
      } else {
        sum2 += arr[i];
      }
    }
    curr = abs(sum2 - sum1);
    if (curr < ans) {
      ans = curr;
    }
  }
  std::cout << ans;
  return 0;
}