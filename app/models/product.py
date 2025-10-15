from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers
import logging
# from html.parser import commentclose
from flask.globals import current_app

# Tabla: product
class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_internal = Column(String(50))
    description = Column(String(255))
    investment = Column(DECIMAL(10, 2))
    client_profile_price = Column(DECIMAL(10, 2))
    client_complete_price = Column(DECIMAL(10, 2))
    product_profit_profile = Column(DECIMAL(10, 2))
    product_profit_per_complete = Column(DECIMAL(10, 2))
    image = Column(String(255))
    total_profiles = Column(Integer)
    active_profiles = Column(Integer)
    available_profiles = Column(Integer)
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))
    access_identifier = Column(String(100))
    access_password = Column(String(100))
    expiration_date = Column(TIMESTAMP)
    comments = Column(String(255))
    contracts = relationship("Contract", back_populates="product", lazy=True)
    
    @staticmethod
    def import_product(data):
        #definimos variables
        cve_internal = None
        product_description = ""
        investment = 0
        client_profile_price = 0
        client_complete_price = 0
        product_status = ""
        product_status_desc = ""
        product_created_by = ""
        product_access_identifier = ""
        product_access_password = ""
        total_profiles = 1  # para evitar división por cero
        product_comments = ""
        product_image = None
        product_expiration_date = None
        product_profit_profile = 0
        product_profit_per_complete = 0
        # description,investment,client_profile_price,client_complete_price,total_profiles,access_identifier,access_password,expiration_date,created_by
        products = Product.calculate_products_by_description(data[0])
        logging.info(f"Products with description: {data[0]} = {products}")
        cve_internal = f"{data[0][:4]}-{products + 1}"
        product_description = data[0]
        investment = data[1]
        client_profile_price = int(data[2]) 
        client_complete_price = int(data[3])
        total_profiles = data[4]
        product_access_identifier = data[5]
        product_access_password = data[6]
        product_status = 1
        product_status_desc = "Activo"
        product_expiration_date = data[8]
        product_created_by = data[7]
        
       
        # product_comments = data[10]
        # product_image = data[11]
        if total_profiles > 0:
            product_profit_profile = client_profile_price - (investment / total_profiles)
            product_profit_per_complete = client_complete_price - product_profit_per_complete
       
        new_product = Product(
            cve_internal=cve_internal,
            description=product_description,
            investment=investment,
            client_profile_price=client_profile_price,
            client_complete_price=client_complete_price,
            status=product_status,
            status_desc=product_status_desc,
            created_by=product_created_by,
            access_identifier=product_access_identifier,
            access_password=product_access_password,
            total_profiles=total_profiles,
            product_profit_profile=product_profit_profile,
            product_profit_per_complete=product_profit_per_complete,
            created_at=datetime.now(),
            active_profiles=0,
            available_profiles=total_profiles,
    
            # comments=product_comments,
            # image=product_image,
            expiration_date = datetime.strptime(product_expiration_date, "%m/%d/%y").date()
        )
        db.session.add(new_product)
        db.session.commit()

        return new_product, "Producto importado correctamente"
    @staticmethod
    def get_by_user_id(user_id):
        logger.info(f"models.py: Getting products by user id: {user_id}")
        products = db.session.query(Product).filter_by(created_by=user_id).all()
        if not products:
            return None
        return products    
    @staticmethod
    def create_new_product(data,imagePath):
        cve_internal = None
        product_description = ""
        investment = 0
        client_profile_price = 0
        client_complete_price = 0
        product_status = ""
        product_status_desc = ""
        product_created_by = ""
        product_access_identifier = ""
        product_access_password = ""
        total_profiles = 1  # para evitar división por cero
        product_comments = ""
        product_image = None
        product_expiration_date = None

        # Clave interna
        if not data.get('cve_internal'):
            products = Product.calculate_products_by_description(data.get('description', ''))
            logger.info(f"Products with description: {data.get('description')} = {products}")

        product_description = data.get('description', '')

        # Conversión segura
        try:
            investment = int(data.get('investment', 0))
        except ValueError:
            logger.warning("Valor inválido para 'investment'")

        try:
            client_profile_price = float(data.get('client_profile_price', 0))
        except ValueError:
            logger.warning("Valor inválido para 'client_profile_price'")

        try:
            client_complete_price = float(data.get('client_complete_price', 0))
        except ValueError:
            logger.warning("Valor inválido para 'client_complete_price'")

        product_status = data.get('status', '') or 1
        product_status_desc = data.get('status_desc', '') or "Activo"
        product_created_by = data.get('created_by', '')
        product_access_identifier = data.get('access_identifier', '')
        product_access_password = data.get('access_password', '')

        try:
            total_profiles = int(data.get('total_profiles'))
        except ValueError:
            logger.warning("Valor inválido para 'total_profiles'")

        product_comments = data.get('comments', '')
        product_image = imagePath  # Asumiendo que imagePath fue definido antes
        product_expiration_date = data.get('expiration_date', '')
                
        try:
            total_profiles = int(data.get('total_profiles', 1))
        except ValueError:
            logger.warning("Valor inválido para 'total_profiles'")
            
        if total_profiles > 0:
            product_profit_profile = client_profile_price - (investment / total_profiles)
        else:
            product_profit_profile = 0

        new_product = Product(
            cve_internal=cve_internal,
            description=product_description,
            investment=investment,
            client_profile_price=client_profile_price,
            client_complete_price=client_complete_price,
            product_profit_profile=product_profit_profile,
            product_profit_per_complete=client_complete_price-investment,
            image=product_image,
            status=1,
            status_desc='Activo',
            created_at=datetime.now(),
            created_by=product_created_by,
            access_identifier=product_access_identifier,
            access_password=product_access_password,
            total_profiles=total_profiles,
            active_profiles=0,
            available_profiles=total_profiles,
            comments=product_comments,
            expiration_date=product_expiration_date
        )
        logger.info(f"Creating new product input received: {data}")   
        logging.info(f"Creating new product: {new_product}") 
        try:
            db.session.add(new_product)
            db.session.flush()
            db.session.commit()
            return new_product, "Product created successfully"
        except Exception as e:
            logger.error(f"Error creating new product: {str(e)}")
            return None
    @staticmethod
    def calculate_products_by_description(description):
        products = Product.query.filter(Product.description.like(f"%{description}%")).all()
        return len(products)
    
    @staticmethod
    def update_product(id, data):
        try:
            # data.update(updated_at = datetime.now()
            current_product = db.session.query(Product).filter_by(id=id).first()
            if not current_product:
                return None
            
            current_product.__dict__.update(data)
            current_product.updated_at = datetime.now()
            # product = db.session.query(Product).filter_by(id=id).update(data)
            db.session.commit()
            return current_product, "Producto actualizado exitosamente"
        except Exception as e: 
            logger.error(f"Error al actualizar producto: {e}")
            return None

    @staticmethod
    def get_by_id(id):
        logger.info(f"models.py: Getting product by id: {id}")
        product = db.session.query(Product).filter_by(id=id).first()
        if not product:
            return None
        else:
            return db.session.query(Product).filter_by(id=id).first()
    @staticmethod
    def get_by_cve_internal(cve_internal):
        logger.info(f"models.py: Getting product by cve_internal: {cve_internal}")
        product = db.session.query(Product).filter_by(cve_internal=cve_internal).first()
        if not product:
            return None
        else:
            return db.session.query(Product).filter_by(cve_internal=cve_internal).first()
    @staticmethod
    def get_by_description(description):
        logger.info(f"models.py: Getting product by description: {description}")
        product = db.session.query(Product).filter_by(description=description).all()
        if not product:
            return None
        else:
            return db.session.query(Product).filter_by(description=description).first()
    @staticmethod
    def get_all():
        logger.info("models.py: Getting all products")
        products = Product.query.all()
        if not products:
            return None
        return products
    
    @staticmethod
    def delete_product(id):
        product = db.session.query(Product).filter_by(id=id).delete()
        db.session.commit()
        return product
    @staticmethod
    def validate_profile_avalailability(product_description):
        # 
        # product = db.session.query(Product).filter_by(description=product_description)..filter_by(status=1).filter_by(Product.available_profiles>0).first()
        product = db.session.execute("SELECT * FROM product WHERE description = :product_description AND status = 1 AND available_profiles > 0", {'product_description': product_description})
        if not product:
            return False
        else:
            print("producto encontrados",product)
            return product
    def to_dict(self):
        return {
            "id": self.id,
            "cve_internal": self.cve_internal,
            "description": self.description,
            "investment": self.investment,
            "client_profile_price": self.client_profile_price,
            "client_complete_price": self.client_complete_price,
            "product_profit_profile": self.product_profit_profile,
            "product_profit_per_complete": self.product_profit_per_complete,
            "image": self.image,
            "total_profiles": self.total_profiles,
            "active_profiles": self.active_profiles,
            "available_profiles": self.available_profiles,
            "status": self.status,
            "status_desc": self.status_desc,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by,
            "access_identifier": self.access_identifier,
            "access_password": self.access_password,
            "comments": self.comments,
            "expiration_date": self.expiration_date
            
        }    