from sanic import Sanic,response
import os
from pydms_config_server.utils import sync_repo


def start_server(cfg):
    app = Sanic()

    @app.route('/<file>')
    async def do_file(request, file):
        file_path = os.path.join(cfg.DATA_DIR, file)
        return await response.file(file_path)
    sync_repo(cfg)
    app.run(host=cfg.HOST, port=cfg.SERVER_PORT, debug=True)