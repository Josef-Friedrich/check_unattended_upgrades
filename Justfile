all: test format docs lint type_check

test:
	uv run --isolated --python=3.10 pytest -m "not (slow or gui)"
	uv run --isolated --python=3.11 pytest -m "not (slow or gui)"
	uv run --isolated --python=3.12 pytest -m "not (slow or gui)"
	uv run --isolated --python=3.13 pytest -m "not (slow or gui)"

test_quick:
	uv run --isolated --python=3.12 pytest

install: update

install_editable: install
	uv pip install --editable .

update:
	uv sync --upgrade

upgrade: update

build:
	uv build

publish:
	uv build
	uv publish

format:
	uv tool run ruff check --select I --fix .
	uv tool run ruff format

docs: docs_readme_patcher

docs_readme_patcher:
	uv tool run --isolated readme-patcher

lint:
	uv tool run ruff check

type_check:
	uv run mypy check_unattended_upgrades.py tests
