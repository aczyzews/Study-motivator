from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    from .views import views
    from .auth import auth
    from .questionaire import questionaire
    from .calendar import calendar
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(questionaire, url_prefix='/')
    app.register_blueprint(calendar, url_prefix='/')
    return app
