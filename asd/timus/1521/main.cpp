#include <cmath>
#include <cstddef>
#include <iostream>
#include <vector>

namespace {
struct SqrtBlock {
  std::size_t sum;
  std::vector<std::size_t> soldiers;
};

std::vector<SqrtBlock> InitCircle(std::size_t n_count) {
  auto n_sqrt_c = static_cast<std::size_t>(std::ceil(std::sqrt(n_count)));
  std::vector<SqrtBlock> circle(n_sqrt_c, {0, {}});

  std::size_t soldier_idx = 1;
  for (std::size_t i = 0; i < n_sqrt_c; i++) {
    while (soldier_idx <= n_count && circle[i].sum < n_sqrt_c) {
      circle[i].soldiers.push_back(soldier_idx);
      circle[i].sum++;
      soldier_idx++;
    }
  }
  return circle;
}

std::size_t FindAndRemove(std::vector<SqrtBlock>& circle, std::size_t pos) {
  for (auto& block : circle) {
    if (pos <= block.sum) {
      const auto offset = static_cast<std::ptrdiff_t>(pos - 1);
      const auto iter = block.soldiers.begin() + offset;
      const std::size_t val = *iter;
      block.soldiers.erase(iter);
      block.sum--;
      return val;
    }
    pos -= block.sum;
  }
  return 0;
}

void ProcessCircle(std::vector<SqrtBlock>& circle, std::size_t n_count, std::size_t k_count) {
  std::size_t current_pos = k_count;
  for (std::size_t m_count = n_count; m_count >= 1; m_count--) {
    const std::size_t soldier_id = FindAndRemove(circle, current_pos);
    std::cout << soldier_id << " ";

    if (m_count > 1) {
      current_pos = (current_pos + k_count - 1) % (m_count - 1);
      if (current_pos == 0) {
        current_pos = (m_count - 1);
      }
    }
  }
}
}  // namespace

int main() {
  std::size_t n_count = 0;
  std::size_t k_count = 0;
  std::cin >> n_count >> k_count;

  std::vector<SqrtBlock> circle = InitCircle(n_count);
  ProcessCircle(circle, n_count, k_count);
  return 0;
}