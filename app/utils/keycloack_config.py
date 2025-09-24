import os
from keycloak import KeycloakAdmin, KeycloakOpenID

# Variables de entorno (recomendado)
# KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080/")
# KEY_CLOAK_USERNAME = os.getenv("KEY_CLOAK_USERNAME", "lordwes")
# KEY_CLOAK_PASSWORD = os.getenv("KEY_CLOAK_PASSWORD", "lordwes")
# KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "crm-users")
# KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "flask-api-client")
# KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "3kAG0TPT1h5qLAclke4ERciH25iWhCyC")


KEYCLOAK_URL = "http://localhost:8080/"
REALM = "crm-users"
CLIENT_ID = "flask-api-client"
CLIENT_SECRET = "3kAG0TPT1h5qLAclke4ERciH25iWhCyC"

KEYCLOAK_SERVER_URL="http://localhost:8080/"
KEYCLOAK_REALM="crm-users"
KEYCLOAK_CLIENT_ID="flask-api-client"
KEYCLOAK_CLIENT_SECRET="CHANGE_ME_SECRET"
KEYCLOAK_REDIRECT_URI="http://localhost:5000/callback"
# Inicializar conexión segura con Keycloak usando service account
keycloak_admin = KeycloakAdmin(
    server_url=KEYCLOAK_SERVER_URL,
    # username=KEY_CLOAK_USERNAME,
    # password=KEY_CLOAK_PASSWORD,
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    verify=False
)

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    verify=False,
)