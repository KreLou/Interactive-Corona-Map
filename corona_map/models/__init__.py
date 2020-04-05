from .case import Case

def init_app(app):
    app.register_blueprint(Case)