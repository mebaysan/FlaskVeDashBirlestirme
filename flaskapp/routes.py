"""Flask uygulamamız için kullandığımız route'lar"""
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    """Anasayfa"""
    return render_template('index.jinja2', title='Açık Kaynak Veri Portalı', )


@app.route('/example')
def example():
    return render_template('example.jinja2', title='Açık Kaynak Veri Portalı | Example', )
