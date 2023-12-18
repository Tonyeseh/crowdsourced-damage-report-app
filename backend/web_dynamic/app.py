#!/usr/bin/python3
""" Web dynamic interface """


from flask import Flask
from os import environ, getcwd

from models import storage
from web_dynamic.admin.views import admin_views
from web_dynamic.workers.views import worker_views
from web_dynamic.users.views import user_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['UPLOAD'] = getcwd()
app.register_blueprint(admin_views)
app.register_blueprint(worker_views)
app.register_blueprint(user_views)

@app.teardown_appcontext
def close_db(error):
    """ close storage """
    storage.close()



if __name__ == "__main__":
    """main function """
    host = environ.get('HOST')
    port = environ.get('PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5002'
    app.run(host=host, port=port, threaded=True, debug=True)
