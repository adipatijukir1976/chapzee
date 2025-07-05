from flask import Blueprint, jsonify, request
from scrape import scrape_paginated_bge_with_page

daftar_bp = Blueprint("daftar", __name__)

@daftar_bp.route("/daftar/<tipe>")
def daftar(tipe):
    page = int(request.args.get("page", 1))
    data = scrape_paginated_bge_with_page(tipe=tipe, page=page)
    return jsonify(data)

