install:
	uv sync

run:
	@uv run python main.py

rcc:
	pyrcc5 resources/resources.qrc -o resources/resources_rc.py

clean:
	rm -rf __pycache__ */*__pycache__ .pytest_cache

setdatabase:
	uv run python services/sql/azenz_database_setup/setup_azenz_databases.py
