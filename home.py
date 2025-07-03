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

    # KOMIK GENRE AKTIF - mengambil genre pertama jika ada
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

    # RESPONSE sesuai tampilan.txt
    return jsonify({
        "home_screen": {
            "menu_utama": {
                "title": "📦 MENU UTAMA",
                "data": menu_utama
            },
            "genre": {
                "title": "🎚️ GENRE",
                "data": genre_list
            },
            "komik_genre_aktif": {
                "title": "🎞️ KOMIK GENRE AKTIF",
                "data": komik_genre_aktif
            },
            "section_komik": {
                "title": "📌 SECTION KOMIK",
                "rekomendasi": {
                    "title": "📚 Rekomendasi",
                    "data": rekomendasi
                }
            },
            "update_baru": {
                "title": "🔥 Update Baru",
                "manga": {
                    "title": "📚 Manga",
                    "data": update_manga
                },
                "manhwa": {
                    "title": "📘 Manhwa",
                    "data": update_manhwa
                },
                "manhua": {
                    "title": "📗 Manhua",
                    "data": update_manhua
                }
            },
            "komik_populer": {
                "title": "🔥 Komik Populer",
                "manga": {
                    "title": "📚 Manga",
                    "data": hot_manga
                },
                "manhwa": {
                    "title": "📘 Manhwa",
                    "data": hot_manhwa
                },
                "manhua": {
                    "title": "📗 Manhua",
                    "data": hot_manhua
                }
            }
        }
    })
