# thirdy party
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
# local
from src.gene.services.meta_service import get_meta
from src.gene.services.gene_service import get_expression_by_gene_id
from src.gene.services.query_service import get_expression_by_ids
from src.gene.utils.validators import (
    ValidationError, 
    validate_meta_request, 
    validate_gene_request,
    validate_expression_query_request)
from src.gene.repository.csv_repository import DatasetSchemaError


expression_bp  = Blueprint("expression", __name__)

# --------------------
# Endpoint for metadata
# --------------------
@expression_bp.route("/<organism>/meta/<feature>", methods=["GET"])
def expression_meta(organism: str, feature: str):
    """
    Endpoint for querying metadata for a dataset.
    A response with an array of objects is expected.
    """
    try:
        # Input validation (user)
        validate_meta_request(
            organism=organism,
            feature=feature,
        )

        # Data processing (use case)
        data = get_meta(
            organism=organism,
            feature=feature,
        )

        # Standard response (success)
        return jsonify({
            "status": "success",
            "message": "Metadata retrieved successfully.",
            "data": data,
        }), 200

    # User input errors
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 400

    # Resource not found
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 404
    
    # File read error
    except IOError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 500

    # Invalid dataset
    except DatasetSchemaError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 500

    # Unexpected error
    except Exception:
        return jsonify({
            "status": "error",
            "message": "Internal server error. Unexpected, please contact the administrator.",
            "data": [],
        }), 500


# --------------------
# Endpoint for single gene expression
# --------------------
@expression_bp.route("/<organism>/<data_type>/<feature>/<gene_id>", methods=["GET"])
def expression_by_gene_id(
    organism: str,
    data_type: str,
    feature: str,
    gene_id: str,
):
    """
    Endpoint to query gene expression by ID.
    A response with an object or empty array is expected.
    """
    try:
        # Input validation (user)
        validate_gene_request(
            organism=organism,
            data_type=data_type,
            feature=feature,
            gene_id=gene_id,
        )

        # Data processing (use case)
        data = get_expression_by_gene_id(
            organism=organism,
            data_type=data_type,
            feature=feature,
            gene_id=gene_id,
        )

        # Dynamic message
        message = (
            f"Expression data retrieved for gene '{gene_id}'."
            if data
            else f"No expression data found for gene '{gene_id}'."
        )

        # Standard response (success)
        return jsonify({
            "status": "success",
            "message": message,
            "data": data,
        }), 200

    # User input errors
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 400

    # Resource not found
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 404
    
    # File read error
    except IOError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 500

    # Invalid dataset
    except DatasetSchemaError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": [],
        }), 500

    # Unexpected error
    except Exception:
        return jsonify({
            "status": "error",
            "message": "Internal server error.",
            "data": [],
        }), 500


# --------------------
# IDS MULTI-QUERY ENDPOINT
# --------------------
@expression_bp.route("/<organism>/<data_type>/<feature>/query", methods=["POST"])
def expression_by_ids(organism: str, data_type: str, feature: str):
    """
    Endpoint for querying multiple gene/transcript expressions.
    Expects to receive a JSON with:
    {
        “ids”: ['id1', 'id2', ...],
        “columns”: ['cond1', 'cond2', ...]
    }
    A response with an array of objects is expected.
    """
    try:
        body = request.get_json()
    except BadRequest:
        # Invalid JSON body
        return jsonify({
            "status": "error",
            "message": "Invalid JSON body, please verify.",
            "data": []
        }), 400
    
    try:

        ids = body.get("ids", [])
        columns = body.get("columns", [])

        # Input validation (user)
        validate_expression_query_request(
            organism=organism,
            data_type=data_type,
            feature=feature,
            ids=ids,
            columns=columns
        )

        # Data processing (use case)
        data, not_found_ids  = get_expression_by_ids(
            organism=organism,
            data_type=data_type,
            feature=feature,
            ids=ids,
            columns=columns
        )

        # Dynamic message
        if data and not not_found_ids:
            message = f"Expression data retrieved for {len(data)} record(s)."
        elif data and not_found_ids:
            message = (
                f"Expression data retrieved for {len(data)} record(s). "
                f"{len(not_found_ids)} ID(s) were not found."
            )
        else:
            message = "No expression data found for the given IDs."

        # Standard response (success)
        response = {
            "status": "success",
            "message": message,
            "data": data
        }

        if not_found_ids:
            response["not_found_ids"] = not_found_ids

        return jsonify(response), 200

    # User input errors
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 400

    # Resource not found
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 404

    # File read error
    except IOError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 500

    # Invalid dataset
    except DatasetSchemaError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 500

    # Unexpected error
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Unexpected server error: {str(e)}",
            "data": []
        }), 500
