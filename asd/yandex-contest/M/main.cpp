#include <algorithm>
#include <array>
#include <cstddef>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct CostMeta {
  bool blocked = false;
  std::size_t value = 0;
};

struct SumMeta {
  bool is_infinity = true;
  std::size_t distance = 0;

  bool operator<(const SumMeta& other) const {
    return !this->is_infinity && (other.is_infinity || this->distance < other.distance);
  }
};

struct Point {
  std::size_t x;
  std::size_t y;
};

struct VertexMeta {
  CostMeta local;
  SumMeta total;
  bool visited = false;
  bool has_prev = false;
  Point prev = {0, 0};
};

class PointNeighborIterator {
public:
  using iterator_category = std::forward_iterator_tag;
  using value_type = Point;
  using difference_type = std::ptrdiff_t;
  using pointer = const Point*;
  using reference = Point;

  PointNeighborIterator(Point center, std::size_t width, std::size_t height, std::size_t index = 0)
      : center_(center), width_(width), height_(height), index_(index) {
    AdvanceToValid();
  }

  reference operator*() const {
    static constexpr std::array<int, 4> KDx = {0, 0, -1, 1};
    static constexpr std::array<int, 4> KDy = {-1, 1, 0, 0};
    return {
        center_.x + static_cast<std::size_t>(KDx.at(index_)),
        center_.y + static_cast<std::size_t>(KDy.at(index_))
    };
  }

  PointNeighborIterator& operator++() {
    ++index_;
    AdvanceToValid();
    return *this;
  }

  PointNeighborIterator operator++(int) {
    PointNeighborIterator tmp = *this;
    ++(*this);
    return tmp;
  }

  friend bool operator==(const PointNeighborIterator& lhs, const PointNeighborIterator& rhs) {
    return lhs.center_.x == rhs.center_.x && lhs.center_.y == rhs.center_.y &&
           lhs.width_ == rhs.width_ && lhs.height_ == rhs.height_ && lhs.index_ == rhs.index_;
  }

  friend bool operator!=(const PointNeighborIterator& lhs, const PointNeighborIterator& rhs) {
    return !(lhs == rhs);
  }

  [[nodiscard]] PointNeighborIterator begin() const {
    return {center_, width_, height_, 0};
  }

  [[nodiscard]] PointNeighborIterator end() const {
    return {center_, width_, height_, 4};
  }

private:
  void AdvanceToValid() {
    static constexpr std::array<int, 4> KDx = {0, 0, -1, 1};
    static constexpr std::array<int, 4> KDy = {-1, 1, 0, 0};
    while (index_ < 4) {
      const int neigh_x = static_cast<int>(center_.x) + KDx.at(index_);
      const int neigh_y = static_cast<int>(center_.y) + KDy.at(index_);
      if (neigh_x >= 0 && static_cast<std::size_t>(neigh_x) < width_ && neigh_y >= 0 &&
          static_cast<std::size_t>(neigh_y) < height_) {
        return;
      }
      ++index_;
    }
  }

  Point center_;
  std::size_t width_;
  std::size_t height_;
  std::size_t index_;
};

class RectangularGraph {
public:
  RectangularGraph(std::vector<std::vector<char>>& matrix, Point start, Point end)
      : end_(end), start_(start) {
    matrix_.resize(matrix.size());
    for (std::size_t i = 0; i < matrix.size(); i++) {
      matrix_[i].reserve(matrix[i].size());
      for (std::size_t j = 0; j < matrix[i].size(); j++) {
        VertexMeta vmeta{};
        vmeta.local = GetCost(matrix[i][j]);
        matrix_[i].push_back(vmeta);
      }
    }
    matrix_[start.y][start.x].total.is_infinity = false;
  }

  static CostMeta GetCost(char vertex) {
    switch (vertex) {
      case '.':
        return {false, 1};
      case 'W':
        return {false, 2};
      default:
        return {true, 0};
    }
  }

  [[nodiscard]] const VertexMeta& GetVertex(Point point) const {
    return matrix_[point.y][point.x];
  }

  const VertexMeta& CalculateShortestPath() {
    struct QueueItem {
      std::size_t distance;
      Point point;
      bool operator>(const QueueItem& other) const {
        return distance > other.distance;
      }
    };

    std::priority_queue<QueueItem, std::vector<QueueItem>, std::greater<QueueItem>> pq;
    pq.push({0, start_});

    while (!pq.empty()) {
      auto [dist, vertex_min] = pq.top();
      pq.pop();

      VertexMeta& vertex_min_meta = this->matrix_[vertex_min.y][vertex_min.x];

      if (vertex_min_meta.visited || dist > vertex_min_meta.total.distance) {
        continue;
      }

      vertex_min_meta.visited = true;

      if (vertex_min.x == end_.x && vertex_min.y == end_.y) {
        break;
      }

      for (auto edge :
           PointNeighborIterator(vertex_min, this->matrix_[0].size(), this->matrix_.size())) {
        VertexMeta& edge_vertex = this->matrix_[edge.y][edge.x];
        if (edge_vertex.local.blocked) {
          continue;
        }

        const std::size_t new_dist = vertex_min_meta.total.distance + edge_vertex.local.value;
        if (edge_vertex.total.is_infinity || new_dist < edge_vertex.total.distance) {
          edge_vertex.total.is_infinity = false;
          edge_vertex.total.distance = new_dist;
          edge_vertex.has_prev = true;
          edge_vertex.prev = vertex_min;
          pq.push({new_dist, edge});
        }
      }
    }
    return this->matrix_[this->end_.y][this->end_.x];
  }

  class PointIterator {
  public:
    using iterator_category = std::forward_iterator_tag;
    using value_type = Point;
    using difference_type = std::ptrdiff_t;
    using pointer = const Point*;
    using reference = Point;

    explicit PointIterator(
        const std::vector<std::vector<VertexMeta>>& matrix, std::size_t row, std::size_t col
    )
        : matrix_(&matrix), row_(row), col_(col) {
    }

    reference operator*() const {
      return Point{col_, row_};
    }

    PointIterator& operator++() {
      if (row_ < matrix_->size()) {
        ++col_;
        if (col_ >= matrix_->at(row_).size()) {
          ++row_;
          col_ = 0;
        }
      }
      return *this;
    }

    PointIterator operator++(int) {
      PointIterator tmp = *this;
      ++(*this);
      return tmp;
    }

    friend bool operator==(const PointIterator& lhs, const PointIterator& rhs) {
      return lhs.row_ == rhs.row_ && lhs.col_ == rhs.col_;
    }

    friend bool operator!=(const PointIterator& lhs, const PointIterator& rhs) {
      return !(lhs == rhs);
    }

  private:
    const std::vector<std::vector<VertexMeta>>* matrix_;
    std::size_t row_;
    std::size_t col_;
  };

  [[nodiscard]] PointIterator begin() const {
    return matrix_.empty() ? end() : PointIterator(matrix_, 0, 0);
  }

  [[nodiscard]] PointIterator end() const {
    return PointIterator(matrix_, matrix_.size(), 0);
  }

  [[nodiscard]] PointIterator iterator() const {
    return begin();
  }

private:
  std::vector<std::vector<VertexMeta>> matrix_;
  const Point end_;
  const Point start_;
};

int main() {
  std::size_t nrow_s = 0;
  std::size_t mcol_s = 0;
  Point start{};
  Point end{};
  std::cin >> nrow_s >> mcol_s >> start.y >> start.x >> end.y >> end.x;

  std::vector<std::vector<char>> matrix(nrow_s);
  for (std::size_t i = 0; i < nrow_s; i++) {
    std::string line;
    std::cin >> line;
    matrix[i].reserve(mcol_s);
    for (const char type : line) {
      matrix[i].push_back(type);
    }
  }

  RectangularGraph graph(matrix, {start.x - 1, start.y - 1}, {end.x - 1, end.y - 1});
  const VertexMeta shortest_path_meta = graph.CalculateShortestPath();
  if (shortest_path_meta.total.is_infinity) {
    std::cout << -1;
    return 0;
  }

  std::cout << shortest_path_meta.total.distance << '\n';

  Point current = {end.x - 1, end.y - 1};
  std::vector<char> directions;
  while (graph.GetVertex(current).has_prev) {
    const Point prev = graph.GetVertex(current).prev;

    const int diff_y = static_cast<int>(current.y) - static_cast<int>(prev.y);
    const int diff_x = static_cast<int>(current.x) - static_cast<int>(prev.x);

    if (diff_y == -1) {
      directions.push_back('N');
    } else if (diff_y == 1) {
      directions.push_back('S');
    } else if (diff_x == -1) {
      directions.push_back('W');
    } else if (diff_x == 1) {
      directions.push_back('E');
    }

    current = prev;
  }

  std::reverse(directions.begin(), directions.end());

  for (const char dir : directions) {
    std::cout << dir;
  }
  std::cout << '\n';
  return 0;
}