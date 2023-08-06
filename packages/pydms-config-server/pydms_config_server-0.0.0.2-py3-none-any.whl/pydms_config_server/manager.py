from sanic import Sanic,response
from .utils import sync_repo,load_json
from .config import DEFAULT_CONFIG_FILE,PKG_ROOT_DIR
from jinja2 import Environment,FileSystemLoader
import os
env=Environment(loader=FileSystemLoader((os.path.join(PKG_ROOT_DIR,'data','templates'))))

def start_management_server(cfg):
    app=Sanic()
    app.static('/static',os.path.join(PKG_ROOT_DIR,'data','static'))
    @app.route('/manage')
    async def do_manage(request):
        text=env.get_template('manage.html').render()
        return response.html(text)
    @app.route('/config')
    async def do_config_get(request):
        return response.json(load_json(DEFAULT_CONFIG_FILE))

    @app.route('/sync')
    async def do_manage(request):
        try:
            await sync_repo(cfg)
        except:
            return response.text('Error occurred on server side.')
        finally:
            return response.text('Sync config files success')
    app.run(cfg.HOST,cfg.MANAGEMENT_PORT,debug=True)
