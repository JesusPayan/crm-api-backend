from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
# from app.routes.microserviceProducts.productsApi import products_api
# from app.routes.microserviceContracts.contractsApi import contracts_api

import os

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)  # <-- Esta línea es nueva
    # Blueprints
    # # from app.routes.client_routes import client_bp
    # app.register_blueprint(client_bp, url_prefix="/api/clients")
    from app.routes.microserviceClients.clientsApi import clients_api
    from app.routes.microservicesProducts.productsApi import products_api
    from app.routes.microserviceContracts.contractsApi import contracts_api
    from app.routes.microserviceCatalogs.catalogsApi import catalogs_api
    from app.routes.test_routes import test_bp
    app.register_blueprint(test_bp)
    app.register_blueprint(clients_api, url_prefix="/v1/clients")
    app.register_blueprint(products_api, url_prefix="/v1/products")
    app.register_blueprint(contracts_api, url_prefix="/v1/contracts")
    app.register_blueprint(catalogs_api, url_prefix="/v1/catalogs")
    
# http://127.0.0.1:5000/v1/clients/api/create

    return app
