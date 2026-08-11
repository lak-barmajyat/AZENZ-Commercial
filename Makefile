PYTHON ?= uv run python

install:
	uv sync

run:
	@$(PYTHON) main.py

rcc:
	pyrcc5 resources/resources.qrc -o resources/resources_rc.py

clean:
	rm -rf __pycache__ */*__pycache__ .pytest_cache

setdatabase:
	uv run python services/sql/azenz_database_setup/setup_azenz_databases.py

# ----------------------------------------------------------------------
# QSS sync: propagate theme/style/base.qss into every window's embedded QSS
# ----------------------------------------------------------------------
sync-qss:
	@$(PYTHON) theme/sync_qss.py sync

qss-check:
	@$(PYTHON) theme/sync_qss.py check

qss-diff:
	@$(PYTHON) theme/sync_qss.py diff

qss-back:
	@$(PYTHON) theme/sync_qss.py back 1

qss-back-back:
	@$(PYTHON) theme/sync_qss.py back 2

qss-backups:
	@$(PYTHON) theme/sync_qss.py list

# ----------------------------------------------------------------------
# Run a single window (preview). Each target launches that window's main.
# Example: make ventes_list
# ----------------------------------------------------------------------
login:
	@$(PYTHON) modules/login/main.py

dashboard:
	@$(PYTHON) modules/table_de_bord/menu/main.py

dashboard_widget:
	@$(PYTHON) modules/table_de_bord/widget/main.py

ventes_list:
	@$(PYTHON) modules/ventes/liste_ventes/main.py

ventes_nouveau_doc:
	@$(PYTHON) modules/ventes/nouveau_doc/main.py

achats_list:
	@$(PYTHON) modules/achats/liste_achats/main.py

achats_nouveau_doc:
	@$(PYTHON) modules/achats/nouveau_doc/main.py

reglements_list:
	@$(PYTHON) modules/reglements/liste_reglements/main.py

reglements_nouveau_reglement:
	@$(PYTHON) modules/reglements/nouveau_reglement/main.py

articles_list:
	@$(PYTHON) modules/articles/liste_articles/main.py

articles_nouveau_article:
	@$(PYTHON) modules/articles/nouveau_article/main.py

familles_list:
	@$(PYTHON) modules/familles/liste_familles/main.py

familles_nouveau_famille:
	@$(PYTHON) modules/familles/nouveau_famille/main.py

clients_list:
	@$(PYTHON) modules/clients/liste_clients/main.py

clients_nouveau_client:
	@$(PYTHON) modules/clients/nouveau_client/main.py

fournisseurs_list:
	@$(PYTHON) modules/fournisseurs/liste_fournisseurs/main.py

fournisseurs_nouveau_fournisseur:
	@$(PYTHON) modules/fournisseurs/nouveau_fournisseur/main.py

stockage_list:
	@$(PYTHON) modules/stockage/liste_stockage/main.py

stockage_nouveau_mouvement:
	@$(PYTHON) modules/stockage/nouveau_mouvement/main.py

parameters_list:
	@$(PYTHON) modules/parameters/liste_parameters/main.py
