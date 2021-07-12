from dotenv import load_dotenv
import os
import errno
import time

# Get variables from .env file
load_dotenv(override=True)

# Useful function
def write_file(filepath,content):
	"Write new file @filepath with @content"
	f = open(filepath,"w+")
	f.write(content)
	f.close()


# Get variables from .env
odoo_admin_pwd = os.getenv("ODOO_ADMIN_PWD")
db_host = os.getenv("ODOO_CONTAINER") + "_db"
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
addons_path = os.getenv("ADDONS_PATH")


# Content to generate odoo.conf
odoo_conf = """
[options]
admin_passwd = {ODOO_ADMIN_PWD}
addons_path = {ADDONS_PATH}
db_host = {DATABASE_HOST}
db_user = {DATABASE_USER}
db_password = {DATABASE_PWD}

# Other odoo conf can be add below

""".format(ODOO_ADMIN_PWD=odoo_admin_pwd,DATABASE_USER=db_user, DATABASE_PWD=db_password,DATABASE_HOST=db_host, ADDONS_PATH=addons_path)

# Create the odoo.conf with info from odoo_conf in the current directory
write_file("./odoo.conf",odoo_conf)
