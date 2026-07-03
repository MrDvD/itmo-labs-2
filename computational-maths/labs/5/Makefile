SHELL := /bin/bash

filepath=report/
filename=main

clean:
	# clean project artifacts
	@for file_ext in "*.pdf" "*.aux" "*.log" "*.toc" "*.out" "*.bbl" "*.blg" "*.bcf" "*.run.xml" "*.txt" "*.compiled.*"; do \
		find $(report_dir) -name "$${file_ext}" -delete; \
	done

build: clean
	cd src && \
	g++ main.cpp -g lib/differential.hpp lib/interpolate.hpp -I. -Ilib -o ../main.bin -std=c++20

generate: clean
	./main.bin ; \
	source ./venv/bin/activate; \
	python src/python/main.py

pdf:
	cd "${filepath}"; \
	xelatex "${filename}"; \
	biber "${filename}"; \
	xelatex "${filename}"