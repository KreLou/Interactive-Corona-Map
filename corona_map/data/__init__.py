from . import region_total, region_history, region_community_grouped

def init_app(app):
    app.register_blueprint(region_total.mod)
    app.register_blueprint(region_history.mod)
    app.register_blueprint(region_community_grouped.mod)