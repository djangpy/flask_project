# 1.vytvorim env premennu 
#   export MDBLOG_CONFIG=/vagrant/configs/delopment.py
# 2. skontrolujem ci MDBLOG_CONFIG obsahuje cestu ku konfiguraku 
#     echo $MDBLOG_CONFIG
# /vagrant/configs/development.py

DEBUG = True
DATABASE = "/vagrant/blog.db"
SQLALCHEMY_DATABASE_URI = "sqlite:////vagrant/blog.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False