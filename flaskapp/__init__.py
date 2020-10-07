"""Flask uygulamamızı oluşturuyoruz"""
from flask import Flask


def init_app():
    """Dash uygulaması ile bind edilmiş çekirdek Flask uygulamamızı inşa ediyoruz"""
    app = Flask(__name__, instance_relative_config=False) # flask uygulaması oluşturuyoruz
    app.config.from_object('config.Config') # kök dizindeki config.py altındaki Config sınıfından uygulama ayarlarını set ediyoruz

    with app.app_context():
        # Çekirdek Flask uygulamamızın bileşenlerini import ediyoruz
        from flaskapp import routes

        # Dash uygulamamızı import ediyoruz
        from flaskapp.dashboard.app import init_dashboard
        app = init_dashboard(app) # dash uygulamamızı oluşturmak için fonksiyonu çalıştırıyoruz ve parametre olarak Flask uygulamamızı yolluyoruz (server olarak)

        return app
