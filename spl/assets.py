# -*- coding: utf-8 -*-

from os import path, makedirs
from flask_assets import Environment, Bundle
from webassets.filter import get_filter

def configure_bundles(app):
    assets = Environment(app)
    assets_out_dir = app.config.get('ASSETS_OUTPUT_DIR')
    # ensure output path exists
    if not path.exists(path.join(app.static_folder, assets_out_dir)):
        app.logger.info("Creating assets output folder")
        makedirs(path.join(app.static_folder, assets_out_dir))

    # webassets bundles
    js_bundle = Bundle(
        'js.old/vendor/require.js',
        'js.old/vendor/jquery-1.9.1.js',
        'js.old/vendor/jquery.dotimeout-1.0.js',
        'js.old/vendor/json2.js',
        'js.old/vendor/underscore-1.4.4.js',
        'js.old/vendor/backbone-0.9.10.js',
        'js.old/spl.resize.design.js',
        'js.old/spl.hover.js',
        'js.old/spl.checkboxes.js',
        'js.old/spl.scroll.js',
        'js.old/spl.tooltip.js',
        'js.old/spl.dropdown.js',
        'js.old/spl.autogrow.js',
        'js.old/spl.paginated.js',
        'js.old/spl.models.js',
        filters='jsmin',
        output=path.join(assets_out_dir, 'js_bundle.js'),
    )

    scss = get_filter('scss', load_paths=['scss', 'scss/tesla'])

    scss_bundle = Bundle(
        'scss/tesla/tesla.scss',
        'scss/spl.scss',
        filters=scss,
        depends=('scss/*.scss', 'scss/tesla/*.scss'),
        output=path.join(assets_out_dir, 'scss_bundle.css'),
    )

    style_bundle = Bundle(
        scss_bundle,
        filters='cssmin',
        output=path.join(assets_out_dir, 'css_bundle.css'),
    )

    assets.register('js_bundle', js_bundle)
    assets.register('style_bundle', style_bundle)
