
import requests
from app.logger import logger
from app.models.catalog import Catalog
from app.models.catalog_values import CatalogValue
from sqlalchemy.exc import SQLAlchemyError
from app import db
# from keycloak import KeycloakAdmin

from app.models.user import User
from flask_session import Session
from keycloak import KeycloakOpenID
import logging
from flask import Blueprint, jsonify, request, redirect, url_for, session
from app.utils.keycloack_config import keycloak_openid, KEYCLOAK_REDIRECT_URI

auth_api = Blueprint('authApi', __name__)
# Configuración Keycloak Admin



# @auth_api.route("/login", methods=["POST"])
# def login_user():
#     data = request.json
#     try:
#         token = keycloak_admin.token(data["username"], data["password"])
#         user_info = keycloak_admin.userinfo(token['access_token'])
#         user = User.get_by_username(data["username"])
#         if not user:
#             return jsonify({"error": "Usuario no encontrado en la base de datos"}), 404
#         user_dict = user.to_dict()
#         user_dict["keycloak_id"] = user_info.get("sub")
#         user_dict["email"] = user_info.get("email")
#         user_dict["first_name"] = user_info.get("firstName")
#         user_dict["last_name"] = user_info.get("lastName")
#         user_dict["phone"] = user_info.get("phone")
#         return jsonify({"token": token, "user": user_dict}), 200
#     except Exception as e:
#         logging.error(f"Error during login: {str(e)}")
#         return jsonify({"error": "Credenciales inválidas"}), 401
@auth_api.route("/register", methods=["POST"])
def register_user():
    data = request.json
    try:
        # creamos el usuario en kaycloak
        user_id = keycloak_admin.create_user({
            "email": data["email"],
            "username": data["email"],  # recomendable
            "enabled": True,
            "firstName": data.get("firstName", ""),
            "lastName": data.get("lastName", ""),
            "attributes": {
                "phone": data["phone"],   # ✅ los campos custom van en attributes
            },  
            "credentials": [{
                "value": data["password"],
                "type": "password",
                "temporary": False
            }]
        })
        data["user_id"] = user_id
        new_user = User.save_new_user(data)
        logging.info(f"User created with id: {user_id}")
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


# ============================
# LOGIN - inicia el flujo OAuth
# ============================
@auth_api.route("/login", methods=["get"])

def login():
    try:
        auth_url = keycloak_openid.auth_url(
            redirect_uri=KEYCLOAK_REDIRECT_URI,
            scope="openid email profile",
            state="random_state_string"
        )
        logging.info(f"Redirecting to Keycloak auth URL: {auth_url}")
        return redirect(auth_url)
    except Exception as e:
        logging.error(f"Error iniciando login: {str(e)}", exc_info=True)
        return jsonify({"error": "Error iniciando login con Keycloak"}), 500


# ===================================
# CALLBACK - Keycloak redirige aquí
# ===================================
@auth_api.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No se recibió código de autorización"}), 400

    try:
        # Intercambiar código por tokens
        token = keycloak_openid.token(
            grant_type="authorization_code",
            code=code,
            redirect_uri=KEYCLOAK_REDIRECT_URI
        )

        # Obtener información del usuario
        userinfo = keycloak_openid.userinfo(token["access_token"])

        # Guardar en sesión
        session["user"] = userinfo
        session["token"] = token

        return jsonify({
            "message": "Login exitoso",
            "user": userinfo,
            "token": token
        })
    except Exception as e:
        logging.error(f"Error en callback: {str(e)}")
        return jsonify({"error": "No se pudo completar el login"}), 500


# ============================
# LOGOUT
# ============================
@auth_api.route("/logout", methods=["GET"])
def logout():
    try:
        refresh_token = session.get("token", {}).get("refresh_token")
        session.clear()

        logout_url = keycloak_openid.logout(
            redirect_uri="http://localhost:5000/",
            refresh_token=refresh_token
        )
        return redirect(logout_url)
    except Exception as e:
        logging.error(f"Error cerrando sesión: {str(e)}")
        return jsonify({"error": "Error cerrando sesión"}), 500