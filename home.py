from flask import Blueprint, jsonify
from api.rekomendasi import get_rekomendasi
from api.update_manga import get_update_manga
from api.update_manhwa import get_update_manhwa
from api.update_manhua import get_update_manhua
from api.hot_manga import get_hot_manga
from api.hot_manhwa import get_hot_manhwa
from api.hot_manhua import get_hot_manhua
from api.manga import get_manga
from api.manhwa import get_manhwa
from api.manhua import get_manhua

home_bp = Blueprint("home", __name__)

@home_bp.route("/home", methods=["GET"])
def home():
    # Menu Utama
    menu = [
        {"title": "Manga", "icon": "/manga.png"},
        {"title": "Manhwa", "icon": "/manhwa.png"},
        {"title": "Manhua", "icon": "/manhua.png"},
    ]

    # Genre (hardcoded)
    genres = [
        {"title": "4-Koma", "slug": "4-koma"},
        {"title": "Action", "slug": "action"},
        {"title": "Action Adventure", "slug": "action-adventure"},
        {"title": "Adaptation", "slug": "adaptation"},
        {"title": "Adult", "slug": "adult"},
        {"title": "Adventure", "slug": "adventure"},
        {"title": "Businessman", "slug": "businessman"},
        {"title": "Comedy", "slug": "comedy"},
        {"title": "Cooking", "slug": "cooking"},
        {"title": "Crime", "slug": "crime"},
        {"title": "Delinquents", "slug": "delinquents"},
        {"title": "Demon", "slug": "demon"},
        {"title": "Demons", "slug": "demons"},
        {"title": "Doujinshi", "slug": "doujinshi"},
        {"title": "Drama", "slug": "drama"},
        {"title": "Ecchi", "slug": "ecchi"},
        {"title": "Fantasy", "slug": "fantasy"},
        {"title": "Game", "slug": "game"},
        {"title": "Gender", "slug": "gender"},
        {"title": "Gender Bender", "slug": "gender-bender"},
        {"title": "Genderswap", "slug": "genderswap"},
        {"title": "Ghosts", "slug": "ghosts"},
        {"title": "Girls' Love", "slug": "girls-love"},
        {"title": "Gore", "slug": "gore"},
        {"title": "Gyaru", "slug": "gyaru"},
        {"title": "Harem", "slug": "harem"},
        {"title": "Hero", "slug": "hero"},
        {"title": "Historical", "slug": "historical"},
        {"title": "Horror", "slug": "horror"},
        {"title": "Isekai", "slug": "isekai"},
        {"title": "Josei", "slug": "josei"},
        {"title": "Kombay", "slug": "kombay"},
        {"title": "Long Strip", "slug": "long-strip"},
        {"title": "Magic", "slug": "magic"},
        {"title": "Manhua", "slug": "manhua"},
        {"title": "Manhwa", "slug": "manhwa"},
        {"title": "Martial Arts", "slug": "martial-arts"},
        {"title": "Mature", "slug": "mature"},
        {"title": "Mecha", "slug": "mecha"},
        {"title": "Medical", "slug": "medical"},
        {"title": "Military", "slug": "military"},
        {"title": "Monsters", "slug": "monsters"},
        {"title": "Murim", "slug": "murim"},
        {"title": "Music", "slug": "music"},
        {"title": "Musical", "slug": "musical"},
        {"title": "Mystery", "slug": "mystery"},
        {"title": "One Shot", "slug": "one-shot"},
        {"title": "Oneshot", "slug": "oneshot"},
        {"title": "Police", "slug": "police"},
        {"title": "Psychological", "slug": "psychological"},
        {"title": "Regresion", "slug": "regresion"},
        {"title": "Regression", "slug": "regression"},
        {"title": "Reincarnation", "slug": "reincarnation"},
        {"title": "Reincarnation Seinen", "slug": "reincarnation-seinen"},
        {"title": "Returner", "slug": "returner"},
        {"title": "Romance", "slug": "romance"},
        {"title": "School", "slug": "school"},
        {"title": "School life", "slug": "school-life"},
        {"title": "Sci-fi", "slug": "sci-fi"},
        {"title": "Seinen", "slug": "seinen"},
        {"title": "Sexual Violence", "slug": "sexual-violence"},
        {"title": "Shotacon", "slug": "shotacon"},
        {"title": "Shoujo", "slug": "shoujo"},
        {"title": "Shoujo Ai", "slug": "shoujo-ai"},
        {"title": "Shounen", "slug": "shounen"},
        {"title": "Shounen Ai", "slug": "shounen-ai"},
        {"title": "Slice of Life", "slug": "slice-of-life"},
        {"title": "Sport", "slug": "sport"},
        {"title": "Sports", "slug": "sports"},
        {"title": "Super Power", "slug": "super-power"},
        {"title": "Superhero", "slug": "superhero"},
        {"title": "Supernatural", "slug": "supernatural"},
        {"title": "Supranatural", "slug": "supranatural"},
        {"title": "Survival", "slug": "survival"},
        {"title": "System", "slug": "system"},
        {"title": "Test System", "slug": "test-system"},
        {"title": "Thriller", "slug": "thriller"},
        {"title": "Time Travel", "slug": "time-travel"},
        {"title": "Tragedy", "slug": "tragedy"},
        {"title": "Vampire", "slug": "vampire"},
        {"title": "Vampires", "slug": "vampires"},
        {"title": "Villainess", "slug": "villainess"},
        {"title": "Web Comic", "slug": "web-comic"},
        {"title": "Wuxia", "slug": "wuxia"},
        {"title": "Yuri", "slug": "yuri"},
    ]

    # Komik berdasarkan genre aktif pertama (misalnya "Action")
    genre_aktif_komik = get_manga()

    # Sections
    sections = {
        "Update Terbaru": get_update_manga() + get_update_manhwa() + get_update_manhua(),
        "Komik Populer": get_hot_manga() + get_hot_manhwa() + get_hot_manhua(),
        "Manga": get_manga(),
        "Manhwa": get_manhwa(),
        "Manhua": get_manhua(),
    }

    return jsonify({
        "menu": menu,
        "genres": genres,
        "komik_genre": genre_aktif_komik,
        "sections": sections
    })
