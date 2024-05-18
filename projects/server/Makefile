export show=all
export revision="head"
export mode="pleasedefine"
export t
export m
export args
export host=localhost
export port=3001

export ORWYNN_DEBUG=1
export ORWYNN_ALLOW_CLEAN=1
export ORWYNN_MODE=dev

test:
	ORWYNN_MODE="test" ORWYNN_DEBUG=1 ORWYNN_ALLOW_CLEAN=1 poetry run coverage run -m pytest -m "not off" -x --ignore=src/legacy -p no:warnings --show-capture=$(show) --failed-first $(args) tests/$(t)

lint:
	poetry run ruff .

check: lint test

coverage:
	poetry run coverage report -m

coverage.html:
	poetry run coverage html --show-contexts && python -m http.server -d htmlcov 8000

run:
	poetry run python -m src $(host) $(port)

