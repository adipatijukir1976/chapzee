from flask import Blueprint, jsonify, request
from scrape import scrape_rekomendasi_bge_with_page

rekomendasi_bp = Blueprint("rekomendasi", __name__)

@rekomendasi_bp.route("/rekomendasi")
def rekomendasi():
    page = int(request.args.get("page", 1))
    data = scrape_rekomendasi_bge_with_page(page=page)
    return jsonify(data)
