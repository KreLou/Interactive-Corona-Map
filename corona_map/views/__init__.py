from . import index, region

def init_app(app):
    app.register_blueprint(index.mod)
    app.register_blueprint(region.mod)