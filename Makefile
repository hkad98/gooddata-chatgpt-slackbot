.PHONY: dev
dev:
	python3.10 -m venv .venv --upgrade-deps
	.venv/bin/pip3 install -r requirements.txt
	.venv/bin/pre-commit install

.PHONY: lint
lint:
	.venv/bin/ruff .

.PHONY: format-fix
format-fix:
	.venv/bin/black .
	.venv/bin/isort .
