# Для Windows используем PowerShell совместимые команды
install:
poetry install

project:
poetry run project

database:
poetry run database

build:
poetry build

publish:
poetry publish --dry-run

package-install:
python -m pip install dist/*.whl

lint:
poetry run ruff check .

format:
poetry run ruff format .
