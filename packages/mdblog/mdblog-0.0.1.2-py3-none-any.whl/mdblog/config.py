import os
import toml


PKG_ROOT_DIR=os.path.dirname(__file__)
PKG_STATIC_DIR=os.path.join(PKG_ROOT_DIR,'data','static')
PKG_TEMPLATE_DIR=os.path.join(PKG_ROOT_DIR,'data','templates')



CONFIG=dict(
    DATA_DIR='./',
    HOST='0.0.0.0',
    PORT=8000
)
