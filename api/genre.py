from flask import Blueprint, jsonify, request
from scrape import scrape_genre_page

genre_bp = Blueprint("genre", __name__)

@genre_bp.route("/genre/<genre>")
def dynamic_genre(genre):
    page = int(request.args.get("page", 1))
    data = scrape_genre_page(genre=genre, page=page)
    return jsonify(data)
