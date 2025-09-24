from flask import Blueprint, jsonify, request
import requests
from app.logger import logger
from app.models.catalog import Catalog
from app.models.catalog_values import CatalogValue
from sqlalchemy.exc import SQLAlchemyError
from app import db
# from keycloak import KeycloakAdmin
from app.utils.keycloack_config import keycloak_admin
import logging

auth_api = Blueprint('authApi', __name__)
# Configuración Keycloak Admin



# @auth_api.route('/register', methods=['POST'])
# def register_user():
#     print("post /register endpoint reached")
#     data = request.json
#     # print(f"Received data: {get_service_token()}")
#     try:
        
#             user_id = keycloak_admin.create_user({
#                 "email": data["email"],
#                 # "username": data["username"],
#                 "enabled": True,
#                 "firstName": data.get("firstName", ""),
#                 "lastName": data.get("lastName", ""),
#                 "credentials": [{
#                     "value": data["password"],
#                     "type": "password",
#                     "temporary": False
#                 }]
#             })
#             logging.info(f"User created with id: {user_id}")
#             return jsonify({"message": "Usuario creado", "user_id": user_id}), 201
#     except Exception as e:
#             logging.info(f"Error creating user: {e}")
#             return jsonify({"error": str(e)}), 400

@auth_api.route("/register", methods=["POST"])
def register_user():
    data = request.json
    try:
        user_id = keycloak_admin.create_user({
            "email": data["email"],
            "username": data["email"],  # recomendable
            "enabled": True,
            "firstName": data.get("firstName", ""),
            "lastName": data.get("lastName", ""),
            "credentials": [{
                "value": data["password"],
                "type": "password",
                "temporary": False
            }]
        })

        return jsonify({"message": "Usuario creado", "user_id": user_id}), 201
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({"error": str(e)}), 400
def get_service_token():
    data = {
        "client_id": "flask-api-client",
        "client_secret": "3kAG0TPT1h5qLAclke4ERciH25iWhCyC",  # KEYCLOAK_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    resp = requests.post(
        f"{'http://localhost:8080/'}/realms/{'crm-users'}/protocol/openid-connect/token",
        data=data,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]