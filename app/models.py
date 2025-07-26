from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers



# Tabla: client
class Client(db.Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_internal = Column(String(50))
    name = Column(String(100))
    mother_lastname = Column(String(100))
    father_lastname = Column(String(100))
    telephone1 = Column(String(20))
    telephone2 = Column(String(20))  # <-- corregido
    email1 = Column(String(100))
    email2 = Column(String(100))
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))

    contracts = relationship("Contract", back_populates="client", lazy=True)

    @staticmethod
    def delete_client(id):
        client = db.session.query(Client).filter_by(id=id).delete()
        db.session.commit()
        return client

    @staticmethod
    def get_all():
        logger.info("models.py: Getting all clients")
        clients = Client.query.all()
        if not clients:
            return None
        return clients
        

    @staticmethod
    def get_by_id(id):
        return db.session.query(Client).filter_by(id=id).first()

    @staticmethod
    def update_client(id, data):
        client = db.session.query(Client).filter_by(id=id).update(data)
        db.session.commit()
        return client

    @staticmethod
    def create_new_client(data):
        logger.info(f"Creating new client input received: {data}")
        new_client = Client(
            name=data.get('name'),
            father_lastname=data.get('father_lastname'),
            mother_lastname=data.get('mother_lastname'),
            status=data.get('status'),
            status_desc=data.get('status_desc'),
            telephone1=data.get('telephone1'),
            telephone2=data.get('telephone2') or data.get('telephone1'),
            email1=data.get('email1'),
            email2=data.get('email2') or data.get('email1'),
            created_by=data.get('created_by'),
            created_at=datetime.now()
        )
        try:
            db.session.add(new_client)
            db.session.flush()
            db.session.commit()
            return new_client
        except Exception as e:
            logger.error(f"Error creating new client: {str(e)}")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "father_lastname": self.father_lastname,
            "mother_lastname": self.mother_lastname,
            "telephone1": self.telephone1,
            "telephone2": self.telephone2,
            "email1": self.email1,
            "email2": self.email2,
            "status": self.status,
            "status_desc": self.status_desc,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by
        }

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
    def to_dict():
        logger.info(f"models.py: Getting product by id: {self.id}")
        return {
                "id":self.id,
                "cve_internal":self.cve_internal,
                "description":self.description,
                "investment":self.investment,
                "client_profile_price":self.client_profile_price,
                "client_complete_price":self.client_complete_price,
                "product_profit_profile":self.product_profit_profile,
                "product_profit_per_complete":self.product_profit_per_complete,
                "image":self.image,
                "total_profiles":self.total_profiles,
                "active_profiles":self.active_profiles,
                "available_profiles":self.available_profiles,
                "status":self.status,
                "status_desc":self.status_desc,
                "created_at":self.created_at,
                "created_by":self.created_by,
                "updated_at":self.updated_at,
                "updated_by":self.updated_by,
                "access_identifier":self.access_identifier,
                "access_password":self.access_password,
                "expiration_date":self.expiration_date
        }
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
class Transaction(db.Model):
    __tablename__ = 'accounting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Transaction_type_id = Column(String(50))
    Transaction_type_desc = Column(String(100))
    # client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    # contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=True)
    Transaction_date = Column(Date)
    Transaction_amount = Column(DECIMAL(10, 2))
    Transaction_description = Column(String(100))
    Transaction_reference = Column(String(100))
    Transaction_status = Column(Integer)
    Transaction_status_desc = Column(String(100))
    
    contract = relationship('Contract', backref='accounting', lazy=True)
    client = relationship('Client', backref='accounting', lazy=True)
    @staticmethod
    def get_all_transactions():
        transactions = db.session.query(Transaction).all()
        return transactions
    def to_dict(self):
        return {
                "id":self.id,
                "Transaction_type_id":self.Transaction_type_id,
                "Transaction_type_desc":self.Transaction_type_desc,
                "Transaction_date":self.Transaction_date,
                "Transaction_amount":self.Transaction_amount,
                "Transaction_description":self.Transaction_description,
                "Transaction_reference":self.Transaction_reference,
                "Transaction_status":self.Transaction_status,
                "Transaction_status_desc":self.Transaction_status_desc
        }
    @staticmethod
    def get_by_id(id):
        transaction = db.session.query(Transaction).filter_by(id=id).first()
        return transaction
    def update_transaction(self, id, data):
        transaction = db.session.query(Transaction).filter_by(id=id).update(data)
        if not transaction:
            return None
        else:
            db.session.commit()
            return transaction
    def delete_transaction(self, id):
        transaction = db.session.query(Transaction).filter_by(id=id).delete()
        db.session.commit()
        return transaction
    def add_transaction(type, amount, client_id, contract_id):
        logger.info(f"Adding transaction with type: {type}, amount: {amount}, client_id: {client_id}, contract_id: {contract_id}")
        
        if amount:
            amount = float(amount)
        if client_id:
            client_id = int(client_id)
        if contract_id:
            contract_id = int(contract_id)
        if type == 1:
            type_desc = "Venta"
            new_transaction = Transaction(
                Transaction_type_id=type,
                Transaction_type_desc=type_desc,
                contract_id=contract_id,  # ← CORRECTO
                client_id=client_id,
                Transaction_date=datetime.now().date(),
                Transaction_amount=amount,
                Transaction_description="Complete"
            )
        elif type == 2:
            type_desc = "Compra"
            new_transaction = Transaction(
            Transaction_type_id=type,
            Transaction_type_desc=type_desc,
            Transaction_date=datetime.now().date(),
            Transaction_amount=amount,
            Transaction_description="Complete"
        )
        
        try:
            db.session.add(new_transaction)
            db.session.flush()
            db.session.commit()
            return new_transaction, "Transacción creada con exito"
        except Exception as e:
            logger.error(f"Error al crear la transacción: {str(e.with_traceback())}")
            return None, "Error al crear la transacción"
        finally:
            db.session.close()
    
    
# Tabla: contracts
class Contract(db.Model):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    contract_type = Column(Integer)
    contract_type_desc = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    days_left = Column(Integer)
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))
    total_price = Column(DECIMAL(10, 2))
    

    client = relationship("Client", back_populates="contracts")
    product = relationship("Product", back_populates="contracts")
    @staticmethod
    def get_all_contracts():
        contracts = db.session.query(Contract).all()
        return contracts
    @staticmethod
    def get_by_id(id):
        contract = db.session.query(Contract).filter_by(id=id).first()
        return contract

    @staticmethod
    def delete_contract(id):
        contract = db.session.query(Contract).filter_by(id=id).delete()
        db.session.commit()
        return contract
    @staticmethod
    def create_contract(client_id,product_name, contract_type, created_by,duration):
        print("contract_type",contract_type)
        logger.info(f"Models: Creating contract with client_id: {client_id}, product_name: {product_name}, contract_type: {contract_type}, created_by: {created_by}")   
        #Tipos de contratos 1: Completa, 2: Perfil, 3 renovacion perfil
        #Si el tipo de contrato es 1 significa que el cliente va a adquirir un perfil
        if contract_type == 1:
        #validamos que haya disponibilidad de perfiles, para el producto seleccionado
            product = db.session.query(Product).filter(Product.description == product_name)\
                                            .filter(Product.status == 1)\
                                            .filter(Product.available_profiles > 0)\
                                            .first()
            
            #si no hay perfiles disponibles se debe regresar el mensaje sin perfiles disponibles
            if not product:
                return False,"Sin perfiles disponibles para el producto seleccionado"
            else:
                current_price = product.client_profile_price
                logger.info(f"Product with description:{product.description} perfiles disponibles = {product.available_profiles}")  
        if contract_type == 2:
            #validamos que haya disponibilidad de cuentas completas
            product = product = db.session.query(Product).filter(Product.description == product_name)\
                                            .filter(Product.status == 1)\
                                            .filter(Product.available_profiles >= Product.total_profiles).first()
            if not product:
                return False,"No hay cuentas disponibles para el producto seleccionado"
            else:
                current_price = product.client_complete_price
                logger.info(f"Product with description:{product.description} perfiles disponibles = {product.available_profiles}")
                                                     
        if product:
            logger.info(f"Product with description:{product.description} perfiles disponibles = {product.available_profiles}")
            contract = Contract(
                client_id=client_id,
                product_id=product.id,
                start_date=datetime.now(),
                contract_type=contract_type,
                #Se asumira que la contratacion es de 30 dias
                end_date=datetime.now() + timedelta(days=duration),
                days_left=duration,
                status=1,
                status_desc="Activo",
                created_at=datetime.now(),
                created_by=created_by,
                updated_at=datetime.now(),
                updated_by=created_by,
                total_price=current_price,
                contract_type_desc= "Perfil" if contract_type == 1 else "Completa"
            )
            try:
                db.session.add(contract)
                db.session.flush()
                db.session.commit()
            except Exception as e:
                logger.error(f"Error creating new contract: {str(e.with_traceback())}")
                return None
            #actualizamos el total de perfiles disponibles
            if contract_type == 1:
                product.available_profiles -= 1
            if contract_type == 2:    
                product.available_profiles -= product.total_profiles
            db.session.commit()
            
            if contract:
                return contract,"Contrato creado exitosamente"
            else:
                return None

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "product_id": self.product_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "status_desc": self.status_desc,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by
        }
# Tabla: catalog
class Catalog(db.Model):
    __tablename__ = 'catalogs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_table = Column(String(50))
    desc_table = Column(String(100))
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))

    values = relationship("CatalogValue", back_populates="catalog")
    @staticmethod
    def get_all_catalogs():
        catalogs = db.session.query(Catalog).all()
        return catalogs
    @staticmethod
    def get_by_id(id):
        catalog = db.session.query(Catalog).filter_by(id=id).first()
        return catalog

    @staticmethod
    def delete_catalog(id):
        catalog = db.session.query(Catalog).filter_by(id=id).delete()
        db.session.commit()
        return catalog
    @staticmethod
    def create_new_catalog(data):
        if data:
                logger.info(f"Creating new catalog: {data}")
                if data['cve_table'] is not None:
                    cve_table = data['cve_table']
                if data['desc_table'] is not None:
                    desc_table = data['desc_table']
                if data['status'] is not None:
                    status = data['status']
                if data['status_desc'] is not None:
                    status_desc = data['status_desc']
                if data['created_by'] is not None:
                    created_by = data['created_by']
    
                catalog = Catalog(
                    cve_table=cve_table,
                    desc_table=desc_table,
                    status=status,
                    status_desc=status_desc,
                    created_at=datetime.now(),
                    created_by=created_by)
                db.session.add(catalog)
                db.session.flush()
                db.session.commit()
                return catalog
        else:
            return None 
    @staticmethod
    def update_catalog_by_id(id, data):
        logger.info(f"Updating catalog with id: {id} and data: {data}")
        try:
            catalog = Catalog.query.filter_by(id=id).first()
            if not catalog:
                return None
            for key, value in data.items():
                if hasattr(catalog, key):
                    setattr(catalog, key, value)
            db.session.commit()
            return catalog
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar catálogo: {str(e)}")
            return None
    
    def to_dict(self):
        return {
            "id": self.id,
            "cve_table": self.cve_table,
            "desc_table": self.desc_table,
            "status": self.status,
            "status_desc": self.status_desc,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by
        }

# Tabla: catalog_values
class CatalogValue(db.Model):
    __tablename__ = 'catalog_values'

    catalog_id = Column(Integer, ForeignKey('catalogs.id'), primary_key=True)
    sequence_id = Column(Integer, primary_key=True)
    key01 = Column(String(100))
    key02 = Column(String(100))
    key03 = Column(String(100))
    key04 = Column(String(100))
    value01 = Column(String(255))
    value02 = Column(String(255))
    value03 = Column(String(255))
    value04 = Column(String(255))
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))

    catalog = relationship("Catalog", back_populates="values")
