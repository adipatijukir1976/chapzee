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
        komik_genre_aktif = {
            "has_next_page": False,
            "page": 1,
            "url": genre_aktif
        }
    else:
        komik_genre_aktif = {
            "has_next_page": False,
            "page": 1,
            "url": None
        }

    # REKOMENDASI
    rekomendasi = {
        "has_next_page": False,
        "page": 1,
        "url": "/rekomendasi"
    }

    # UPDATE BARU
    update_manga = {
        "has_next_page": False,
        "page": 1,
        "url": "/update/manga"
    }
    update_manhwa = {
        "has_next_page": False,
        "page": 1,
        "url": "/update/manhwa"
    }
    update_manhua = {
        "has_next_page": False,
        "page": 1,
        "url": "/update/manhua"
    }

    # KOMIK POPULER
    hot_manga = {
        "has_next_page": False,
        "page": 1,
        "url": "/hot/manga"
    }
    hot_manhwa = {
        "has_next_page": False,
        "page": 1,
        "url": "/hot/manhwa"
    }
    hot_manhua = {
        "has_next_page": False,
        "page": 1,
        "url": "/hot/manhua"
    }

    # RESPONSE sesuai contoh JSON yang diminta
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
                    "title": "📚 Manhwa",
                    "data": update_manhwa
                },
                "manhua": {
                    "title": "📚 Manhua",
                    "data": update_manhua
                }
            },
            "komik_populer": {
                "title": "🔥 Populer",
                "manga": {
                    "title": "📚 Manga",
                    "data": hot_manga
                },
                "manhwa": {
                    "title": "📚 Manhwa",
                    "data": hot_manhwa
                },
                "manhua": {
                    "title": "📚 Manhua",
                    "data": hot_manhua
                }
            }
        }
    })
