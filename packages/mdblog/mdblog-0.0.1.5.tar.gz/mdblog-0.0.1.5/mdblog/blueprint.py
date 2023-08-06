from sanic import Sanic,response,Blueprint
from . import config as cfg
from .config import CONFIG
from .utils import join_path,backslash_required
import os
from jinja2 import Environment,FileSystemLoader
env=Environment(loader=FileSystemLoader(cfg.PKG_TEMPLATE_DIR))

def get_true_path(user,relpath):
    base_dirs = {
        "static":cfg.PKG_STATIC_DIR,
        "user/file":CONFIG['DATA_DIR'],
    }
    root_path=base_dirs[user]
    return join_path(root_path,relpath)
#
class services:
    @staticmethod
    async def send_file(user,rel_path):
        print('sending file %s'%(rel_path))
        true_path=get_true_path(user,rel_path)
        if not os.path.exists(true_path):
            return response.text('File not exists.')
        elif os.path.isdir(true_path):
            return response.text(' Is a directory, not a file.')
        else:
            return await response.file(true_path)
    @staticmethod
    def list_dir(user,rel_path):
        true_path=get_true_path(user,rel_path)
        items = os.listdir(true_path)
        dirs = []
        files = []
        for item in items:
            item_path = os.path.join(true_path, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            elif os.path.isfile(item_path):
                files.append(item)
        return response.html(env.get_template('view-folder.html').render(dirs=dirs, files=files))
    @staticmethod
    def view_md(user,rel_path):
        print('viewing md %s'%(rel_path))
        return  response.html(env.get_template('view.html').render(user=user,path=rel_path))
    @staticmethod
    def view_dir(user,rel_path,smart=True):
        true_path=get_true_path(user,rel_path)
        print('view_dir %s'%(rel_path))
        if os.path.isdir(true_path):
            children = os.listdir(true_path)
            if smart:
                for child in children:
                    if child.lower() == 'readme.md':
                        child_rel_path = os.path.join(rel_path, child)
                        # print(child_rel_path)
                        return services.view_md(user,child_rel_path)
            return services.list_dir(user,rel_path)
        return response.text('Not a directory.')
    @staticmethod
    async def view_path(user,rel_path):
        print('viewing path %s'%(rel_path))
        true_path=get_true_path(user,rel_path)
        if not os.path.exists(true_path):
            return response.text('File or directory not exists.')
        if rel_path.endswith('/'):
            return services.view_dir(user,rel_path)
        else:
            if true_path.lower().endswith('.md'):
                return services.view_md(user,rel_path)
            else:
                return await services.send_file(user,rel_path)
class bp_wrappers:
    @staticmethod
    def wrap_md_viewer(bp,static_dir=cfg.PKG_STATIC_DIR):
        assert isinstance(bp, (Blueprint,Sanic))
        bp.static('/static',static_dir)
        @bp.route('/')
        async def do_root(request):
            return response.redirect('/user/')
        # @bp.route('/static/<path:path>')
        # async def do_file_get(request,path):
        #     return await services.send_file('static',path)
        @bp.route('/user/file/<path:path>')
        async def do_file_get(request,path):
            return await services.send_file('user/file',path)
        @bp.route('/user/')
        @backslash_required
        async def do_user_root(request):
            return services.view_dir('user/file','/')
        @bp.route('/user/<path:path>')
        async def do_view_path(request,path):
            return await services.view_path('user/file',path)
        return bp

