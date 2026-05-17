#include <cstddef>
#include <iostream>
#include <list>
#include <unordered_map>
#include <vector>

struct Vertex {
  bool visited = false;
  std::size_t color = 0;
  std::vector<std::size_t> neighbours;
};

class Graph {
public:
  void AddEdge(std::size_t from_id, std::size_t to_id) {
    if (this->vertices_.count(from_id) == 0U) {
      this->vertices_[from_id] = {false, 0, {}};
    }
    if (from_id == to_id) {
      return;
    }
    this->vertices_[from_id].neighbours.push_back(to_id);
  }

  std::size_t CountSources() {
    std::size_t sources_count = 0;
    std::size_t current_color = 0;
    for (std::size_t i = 1; i <= this->vertices_.size(); i++) {
      if (this->vertices_[i].visited) {
        continue;
      }
      std::list<std::size_t> to_visit = {i};
      std::size_t broken_count = 1;
      while (!to_visit.empty()) {
        Vertex& top_vertex = this->vertices_[to_visit.front()];
        to_visit.pop_front();
        top_vertex.visited = true;
        top_vertex.color = current_color;
        for (const auto& neightbour : top_vertex.neighbours) {
          const Vertex& neightbour_vertex = this->vertices_[neightbour];
          if (neightbour_vertex.visited && neightbour_vertex.color != current_color) {
            broken_count = 0;
            continue;
          }
          if (neightbour_vertex.visited) {
            continue;
          }
          to_visit.push_front(neightbour);
        }
      }
      sources_count += broken_count;
      current_color++;
    }
    return sources_count;
  }

private:
  std::unordered_map<std::size_t, Vertex> vertices_;
};

int main() {
  std::size_t n_count = 0;
  std::cin >> n_count;
  Graph graph;
  for (std::size_t i = 1; i <= n_count; i++) {
    std::size_t open_idx = 0;
    std::cin >> open_idx;
    // inverting the direction
    graph.AddEdge(i, open_idx);
  }
  std::cout << graph.CountSources();
  return 0;
}