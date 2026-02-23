#include <bits/stdc++.h>

#include <iostream>
#include <stack>
#include <unordered_map>

using scope = std::unordered_map<std::string, long>;

void update_scope(std::stack<scope>& ctx, scope& vars, std::string lval, std::string rval) {
  char* fail;
  long rval_long = std::strtol(rval.c_str(), &fail, 10);
  if (ctx.top().count(lval) == 0) {
    ctx.top()[lval] = vars.count(lval) ? vars[lval] : 0;
  }
  if (*fail) {
    vars[lval] = vars[rval];
    std::cout << vars[lval] << "\n";
  } else {
    vars[lval] = rval_long;
  }
}

int main() {
  std::string line;
  scope vars;
  std::stack<scope> ctx;
  ctx.push({});
  while (std::getline(std::cin, line)) {
    if (line == "{") {
      ctx.push({});
    } else if (line == "}") {
      for (const auto& [key, value] : ctx.top()) {
        vars[key] = value;
      }
      ctx.pop();
    } else {
      std::stringstream ss(line);
      std::string lval, rval;
      std::getline(ss, lval, '=');
      std::getline(ss, rval, '=');
      update_scope(ctx, vars, lval, rval);
    }
  }
  return 0;
}