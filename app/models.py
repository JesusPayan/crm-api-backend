# from flask import Flask
# from app import db
# from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
# from sqlalchemy.orm import relationship
# from app.logger import logger
# from datetime import datetime, timedelta
# from flask import jsonify
# import numbers



# # Tabla: contracts

# # Tabla: catalog

# # Tabla: catalog_values
# class CatalogValue(db.Model):
#     __tablename__ = 'catalog_values'

#     catalog_id = Column(Integer, ForeignKey('catalogs.id'), primary_key=True)
#     sequence_id = Column(Integer, primary_key=True)
#     key01 = Column(String(100))
#     key02 = Column(String(100))
#     key03 = Column(String(100))
#     key04 = Column(String(100))
#     value01 = Column(String(255))
#     value02 = Column(String(255))
#     value03 = Column(String(255))
#     value04 = Column(String(255))
#     status = Column(Integer)
#     status_desc = Column(String(100))
#     created_at = Column(TIMESTAMP)
#     created_by = Column(String(100))
#     updated_at = Column(TIMESTAMP)
#     updated_by = Column(String(100))

#     catalog = relationship("Catalog", back_populates="values")
