from flask import Blueprint, jsonify, request
from scrape import scrape_paginated_bge_with_page

update_bp = Blueprint("update", __name__)

@update_bp.route("/update")
def update():
    tipe = request.args.get("tipe", "manga")
    page = int(request.args.get("page", 1))
    data = scrape_paginated_bge_with_page(tipe=tipe, page=page)
    return jsonify(data)
