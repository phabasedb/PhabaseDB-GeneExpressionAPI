from flask import Blueprint, jsonify, request
from .functions import get_gene_data, get_meta_data, get_gene_ids_columns_data

main_bp = Blueprint("main", __name__)

@main_bp.route('/gene/<path:dataset>/<gene_id>', methods=['GET'])
def expression_gene_id(dataset: str, gene_id: str):
    response, status_code = get_gene_data(dataset, gene_id)
    return jsonify(response), status_code

@main_bp.route('/gene/ids', methods=['POST'])
def expression_query():
    data = request.get_json() or {}
    response, status_code = get_gene_ids_columns_data(data.get("dataset",""), data.get("gene_ids",[]), data.get("columns",[]))
    return jsonify(response), status_code

@main_bp.route('/metadata/<path:dataset>', methods=['GET'])
def expression_meta_data(dataset: str):
    response, status_code = get_meta_data(dataset)
    return jsonify(response), status_code