# Run all recipes
all: upgrade test format docs lint type_check

# Execute the tests
test:
	uv run --isolated --python=3.10 pytest
	uv run --isolated --python=3.11 pytest
	uv run --isolated --python=3.12 pytest
	uv run --isolated --python=3.13 pytest

# Execute the quick tests
test_quick:
	uv run --isolated --python=3.12 pytest

# Install the dependencies (alias of upgrade)
install: upgrade

# Install the editable package based on the provided local file path
install_editable: install
	uv pip install --editable .

# Upgrade the dependencies
upgrade:
	uv sync --upgrade

# Upgrade the dependencies (alias of upgrade)
update: upgrade

# Build Python packages into source distributions and wheels
build:
	uv build

# Upload distributions to an index
publish:
	uv build
	uv publish

# Run ruff format
format:
	uv tool run ruff check --select I --fix .
	uv tool run ruff format

# Build the documentation
docs: docs_readme_patcher

# Generate the README file using the readme-patcher
docs_readme_patcher:
	uv tool run --isolated --no-cache readme-patcher


# Run ruff check
lint:
	uv tool run ruff check

# Perform type checking using mypy
type_check:
	uv run mypy src/check_unattended_upgrades tests
