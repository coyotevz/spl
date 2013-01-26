# -*- coding: utf-8 -*-

from os import path, makedirs
from flask.ext.assets import Environment

def configure_bundles(app):
    assets = Environment(app)
    assets_out_dir = app.config.get('ASSETS_OUTPUT_DIR')
    # ensure output path exists
    if not path.exists(path.join(app.static_folder, assets_out_dir)):
        app.logger.info("Creating assets output folder")
        makedirs(path.join(app.static_folder, assets_out_dir))

    with app.open_resource('assets.yaml') as af:
        assets.from_yaml(af)
