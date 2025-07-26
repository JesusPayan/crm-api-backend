from flask import Blueprint, jsonify
from app.models.catalog_values import CatalogValue
from app.models.catalog import Catalog
from app.models.contract import Contract
from app.models.product import Product
from app.models.client import Client
from app.logger import logger

test_bp = Blueprint("test", __name__)

@test_bp.route("/test/clients")
def get_clients():
    return jsonify([c.to_dict() for c in Client.query.all()])

@test_bp.route("/test/products")
def get_products():
    return jsonify([{
        "id": p.id,
        "description": p.description,
        "price": str(p.price),
        "status_desc": p.status_desc
    } for p in Product.query.all()])

@test_bp.route("/test/contracts")
def get_contracts():
    return jsonify([{
        "id": c.id,
        "client": c.client.name,
        "product": c.product.description,
        "start_date": c.start_date.isoformat(),
        "end_date": c.end_date.isoformat()
    } for c in Contract.query.all()])

@test_bp.route("/test/catalogs")
def get_catalogs():
    return jsonify([{
        "id": cat.id,
        "cve_table": cat.cve_table,
        "desc_table": cat.desc_table
    } for cat in Catalog.query.all()])

@test_bp.route("/test/catalog-values")
def get_catalog_values():
    return jsonify([{
        "catalog_id": val.catalog_id,
        "key01": val.key01,
        "value01": val.value01
    } for val in CatalogValue.query.all()])