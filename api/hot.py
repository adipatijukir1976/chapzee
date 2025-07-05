from flask import Blueprint, jsonify, request
from scrape import scrape_hot_bge_with_page

hot_bp = Blueprint("hot", __name__)

@hot_bp.route("/hot/<tipe>")
def hot(tipe):
    page = int(request.args.get("page", 1))
    data = scrape_hot_bge_with_page(tipe=tipe, page=page)
    return jsonify(data)

