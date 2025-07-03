from flask import Flask, jsonify
from daftar import daftar_bp
from genre import genre_bp
from hot import hot_bp
from rekomendasi import rekomendasi_bp
from update import update_bp

app = Flask(__name__)

# Register semua blueprint
app.register_blueprint(daftar_bp)
app.register_blueprint(genre_bp)
app.register_blueprint(hot_bp)
app.register_blueprint(rekomendasi_bp)
app.register_blueprint(update_bp)

# HOME ENDPOINT
@app.route("/home")
def home():
    # MENU UTAMA
    menu_utama = [
        {"title": "Manga", "icon": "📘"},
        {"title": "Manhua", "icon": "📗"},
        {"title": "Manhwa", "icon": "📙"}
    ]

    # GENRE LIST
    from scrape import scrape_genre_all
    genre_list = scrape_genre_all()

    # KOMIK GENRE AKTIF - contoh mengambil genre pertama jika ada
    if genre_list:
        from scrape import scrape_genre_page
        genre_aktif = genre_list[0]['slug'] if 'slug' in genre_list[0] else genre_list[0]['title']
        komik_genre_aktif = scrape_genre_page(genre=genre_aktif, page=1)
    else:
        komik_genre_aktif = []

    # REKOMENDASI
    from scrape import scrape_rekomendasi_bge_with_page
    rekomendasi = scrape_rekomendasi_bge_with_page(page=1)

    # UPDATE BARU
    from scrape import scrape_paginated_bge_with_page
    update_manga = scrape_paginated_bge_with_page(tipe="manga", page=1)
    update_manhwa = scrape_paginated_bge_with_page(tipe="manhwa", page=1)
    update_manhua = scrape_paginated_bge_with_page(tipe="manhua", page=1)

    # KOMIK POPULER
    from scrape import scrape_hot_bge_with_page
    hot_manga = scrape_hot_bge_with_page(tipe="manga", page=1)
    hot_manhwa = scrape_hot_bge_with_page(tipe="manhwa", page=1)
    hot_manhua = scrape_hot_bge_with_page(tipe="manhua", page=1)

    # RESPONSE
    return jsonify({
        "menu_utama": menu_utama,
        "genre": genre_list,
        "komik_genre_aktif": komik_genre_aktif,
        "rekomendasi": rekomendasi,
        "update_baru": {
            "manga": update_manga,
            "manhwa": update_manhwa,
            "manhua": update_manhua
        },
        "komik_populer": {
            "manga": hot_manga,
            "manhwa": hot_manhwa,
            "manhua": hot_manhua
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
