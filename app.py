from flask import Flask
from api.daftar import daftar_bp
from api.hot import hot_bp
from api.update import update_bp
from api.rekomendasi import rekomendasi_bp
from api.genre import genre_bp

app = Flask(__name__)

app.register_blueprint(daftar_bp)
app.register_blueprint(hot_bp)
app.register_blueprint(update_bp)
app.register_blueprint(rekomendasi_bp)
app.register_blueprint(genre_bp)

@app.route("/")
def index():
    return {"message": "Komiku Scraper API v2"}
