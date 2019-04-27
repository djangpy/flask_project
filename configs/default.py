# chybová hláška hovorí, že v konfigurácií applikácie (reprezentovaná ako python dictionary) chýba kľúč DATABASE.
# Fix spočíva v tom, že definujeme konfiguráciu appky cez environment premennú. 
# Ten konfigurák je vo /vagrant/configs/development.py
# (venv)$ export MDBLOG_CONFIG=/vagrant/configs/development.py

SECRET_KEY = '(\xe2\x10.\xb3\xdfL[d\x1f\x93\x90\xc2,\xffL\x03N\xc7[G\xa0\xd6\x83'
USERNAME = "admin"
PASSWORD = "admin"
