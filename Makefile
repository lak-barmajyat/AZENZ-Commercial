install:
	uv sync

run:
	uv run python3 main.py

rcc:
	pyrcc5 resources.qrc -o resources_rc.py

clean:
	rm -rf __pycache__ */*__pycache__ .pytest_cache
