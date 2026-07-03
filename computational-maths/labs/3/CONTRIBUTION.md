# Разработка

Команда для компиляции тестов:
```bash
cd src &&
g++ main.cpp -g lib/gauss.cpp lib/random.cpp lib/output.cpp -I. -Ilib -o ../main.out -std=c++20
```