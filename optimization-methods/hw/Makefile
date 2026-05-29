SHELL := /bin/bash

report_dir=report/
report_name=main

config_name=config.yaml

clean:
	# clean LaTeX artifacts
	@for file_ext in "*.pdf" "*.aux" "*.log" "*.toc" "*.out"; do \
		find $(report_dir) -name "$${file_ext}" -delete; \
	done
	# clean project artifacts
	rm -rf $$(grep "output_dir:" ${config_name} | cut -d '"' -f 2)
generate: clean
	source ./venv/bin/activate; \
	python src/main.py
pdf: generate
	cd "${report_dir}"; \
	xelatex "${report_name}"; \
	xelatex "${report_name}"