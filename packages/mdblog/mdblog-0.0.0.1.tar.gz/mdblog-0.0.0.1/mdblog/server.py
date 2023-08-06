from sanic import Sanic,response,Blueprint
from . import config as cfg
from .config import CONFIG
from .blueprint import bp_wrappers
import os

def start_server(host=CONFIG['HOST'],port=CONFIG['PORT']):
    app = Sanic()
    bp_view=bp_wrappers.wrap_md_viewer(Blueprint('bp_view',url_prefix='/'))
    app.blueprint(bp_view)
    app.run(host=host,port=port)