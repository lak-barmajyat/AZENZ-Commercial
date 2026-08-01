install:
	uv sync

run:
	@uv run python main.py

rcc:
	pyrcc5 resources/resources.qrc -o resources/resources_rc.py

clean:
	rm -rf __pycache__ */*__pycache__ .pytest_cache

setdatabase:
	python ./services/sql/db_setup.py