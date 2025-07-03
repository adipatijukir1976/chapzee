from flask import Blueprint, jsonify
from scrape import (
    scrape_genre_all,
    scrape_genre_page,
    scrape_rekomendasi_bge_with_page,
    scrape_paginated_bge_with_page,
    scrape_hot_bge_with_page
)

home_bp = Blueprint("home", __name__)

@home_bp.route("/home")
def home():
    # MENU UTAMA
    menu_utama = [
        {"title": "Manga", "icon": "📘"},
        {"title": "Manhua", "icon": "📗"},
        {"title": "Manhwa", "icon": "📙"}
    ]

    # GENRE LIST
    genre_list = scrape_genre_all()

    # KOMIK GENRE AKTIF - contoh mengambil genre pertama jika ada
    if genre_list:
        genre_aktif = genre_list[0]['slug']
        komik_genre_aktif = scrape_genre_page(genre=genre_aktif, page=1)
    else:
        komik_genre_aktif = []

    # REKOMENDASI
    rekomendasi = scrape_rekomendasi_bge_with_page(page=1)

    # UPDATE BARU
    update_manga = scrape_paginated_bge_with_page(tipe="manga", page=1)
    update_manhwa = scrape_paginated_bge_with_page(tipe="manhwa", page=1)
    update_manhua = scrape_paginated_bge_with_page(tipe="manhua", page=1)

    # KOMIK POPULER
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
