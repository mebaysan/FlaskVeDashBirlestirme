from flaskapp import init_app  # __init__.py içerisinden fonksiyonu çağırıyoruz

app = init_app()  # app'imizi oluşturuyoruz

if __name__ == "__main__":  # bu dosya çalıştığında uygulamayı ayağa kaldırıyoruz
    app.run(host='0.0.0.0')
