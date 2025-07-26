from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers

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
    
    contracts = relationship("Contract", back_populates="product", lazy=True)
    
    @staticmethod
    def create_new_product(data):
        if data.get('cve_internal') is None:
            #calculate cve
            products = Product.calculate_products_by_description(data.get('description'))
            logger.info(f"Products with description:{data.get('description')} = {products}")
            cve_internal = f"{data.get('description', '')[:4]}-{products + 1}"
        if data.get('description'):
            product_description = data['description']
        if data.get('price'):
            investment = data['price']
        if data.get('client_profile_price'):
            client_profile_price = data['client_profile_price']
        if data.get('client_complete_price'):
            client_complete_price = data['client_complete_price']
        if data.get('status'):
            product_status = data['status']
        if data.get('status_desc'):
            product_status_desc = data['status_desc']
        if data.get('created_by'):
            product_created_by = data['created_by']
        if data.get('access_identifier'):
            product_access_identifier = data['access_identifier']
        if data.get('access_password'):
            product_access_password = data['access_password']
        if data.get('total_profiles'):
            total_profiles = data['total_profiles']

                
        # expiration_date and image is pending before frontend conection is done
        # if data.get('expiration_date'):
        #         product_expiration_date = data['expiration_date']
        # if data.get('image'):
        #     product_image = data['image']

        new_product = Product(
            cve_internal=cve_internal,
            description=product_description,
            investment=investment,
            client_profile_price=client_profile_price,
            client_complete_price=client_complete_price,
            product_profit_profile=client_profile_price-(int(investment)/int(total_profiles)),
            product_profit_per_complete=client_complete_price-investment,
            # image=product_image,
            status=product_status,
            status_desc=product_status_desc,
            created_at=datetime.now(),
            created_by=product_created_by,
            access_identifier=product_access_identifier,
            access_password=product_access_password,
            total_profiles=total_profiles,
            active_profiles=total_profiles,
            available_profiles=total_profiles
            # 
            # expiration_date=product_expiration_date,
        )
        logger.info(f"Creating new product input received: {data}")    
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
        product = db.session.query(Product).filter_by(id=id).update(data)
        if not product:
            return None
        else:
            db.session.commit()
            return product
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
            "expiration_date": self.expiration_date
        }    