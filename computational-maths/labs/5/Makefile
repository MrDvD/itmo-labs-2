filepath=report/
filename=main

build:
	cd src && \
	g++ main.cpp -g lib/integration.hpp -I. -Ilib -o ../main.out -std=c++20

pdf:
	cd "${filepath}"; \
	xelatex "${filename}"; \
	biber "${filename}"; \
	xelatex "${filename}"