from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers



# Tabla: contracts

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
