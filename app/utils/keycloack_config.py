import os
import logging
from keycloak import KeycloakAdmin, KeycloakOpenID
import jwt  # pip install PyJWT

logging.basicConfig(level=logging.INFO)

keycloak_admin = None
keycloak_openid = None

try:
    # Variables de entorno
    KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080/")
    KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "crm-users-II")
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "flask-api-client")
    KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "CHANGE_ME_SECRET")

    # Inicializamos OpenID (para login / callback)
    keycloak_openid = KeycloakOpenID(
        server_url=KEYCLOAK_SERVER_URL,
        client_id=KEYCLOAK_CLIENT_ID,
        realm_name=KEYCLOAK_REALM,
        client_secret_key=KEYCLOAK_CLIENT_SECRET,
        verify=True,
    )

    # Obtenemos token del Service Account
    token = keycloak_openid.token(grant_type=["client_credentials"])
    access_token = token.get("access_token")

    # Debug de roles incluidos en el token
    decoded_token = jwt.decode(access_token, options={"verify_signature": False})
    print("🔑 Service Account Token obtenido correctamente")
    print("🎭 Realm roles:", decoded_token.get("realm_access", {}))
    print("👤 Client roles:", decoded_token.get("resource_access", {}))

    # Inicializamos KeycloakAdmin SOLO con service account
    keycloak_admin = KeycloakAdmin(
        server_url=KEYCLOAK_SERVER_URL,
        realm_name=KEYCLOAK_REALM,
        client_id=KEYCLOAK_CLIENT_ID,
        client_secret_key=KEYCLOAK_CLIENT_SECRET,
        verify=True,
    )

except Exception as e:
    logging.error(f"❌ Error al inicializar Keycloak: {e}")
    keycloak_admin = None