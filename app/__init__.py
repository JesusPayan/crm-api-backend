from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
from keycloak import KeycloakAdmin
from flask_session import Session
from keycloak import KeycloakOpenID

# from app.routes.microserviceProducts.productsApi import products_api
# from app.routes.microserviceContracts.contractsApi import contracts_api

import os

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    # se cargan las variables de entorno
    load_dotenv()
    # se detecta el entorno que se esta ejecutando
    env = os.getenv('FLASK_ENV', 'development')
    print(f"Entorno: {env}")
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # UPLOAD_FOLDER = 'uploads'
    # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = '!secret'
    
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    if env == 'development':
        print("ENTORNO DESARROLLO")
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL_DEV')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER_LOCAL')
    elif env == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL_TEST')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL_PROD')
        UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER_PROD')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    from app.routes.microserviceClients.clientsApi import clients_api
    from app.routes.microservicesProducts.productsApi import products_api
    from app.routes.microserviceContracts.contractsApi import contracts_api
    from app.routes.microserviceCatalogs.catalogsApi import catalogs_api
    from app.routes.microserviceTransactions.transactionsApi import transaction_api
    from app.routes.microserviceTickets.ticketsApi import tickets_api
    from app.routes.microserviceAuth.authApi import auth_api
    
    from app.routes.test_routes import test_bp
    app.register_blueprint(test_bp)
    app.register_blueprint(clients_api, url_prefix="/v1/clients")
    app.register_blueprint(products_api, url_prefix="/v1/products")
    app.register_blueprint(contracts_api, url_prefix="/v1/contracts")
    app.register_blueprint(catalogs_api, url_prefix="/v1/catalogs")
    app.register_blueprint(transaction_api, url_prefix="/v1/transactions")
    app.register_blueprint(tickets_api, url_prefix="/v1/tickets")
    app.register_blueprint(auth_api, url_prefix="/v1/auth")
    print("\n📜 Rutas registradas en Flask:")
    
    for rule in app.url_map.iter_rules():
        methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        print(f"{methods:10} {rule}")
# http://127.0.0.1:5000/v1/clients/api/create

    return app
