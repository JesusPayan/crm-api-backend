# from app import db
# from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, DECIMAL
# from sqlalchemy.sql import text
# from app.models.contract import Contract
# class ContractSummary(db.Model):
#     __tablename__ = 'contract_sumary'

#     id = Column(Integer, primary_key=True)
#     client_name = Column(String(255))
#     product_name = Column(String(255))
#     contract_type_desc = Column(String(100))
#     start_date = Column(Date)
#     end_date = Column(Date)
#     status_desc = Column(String(100))
#     total_price = Column(DECIMAL(10, 2))
#     created_at = Column(TIMESTAMP)

#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}

#     @staticmethod
#     def get_all():
#         try:
#             # contracts = db.session.query(ContractSummary).all()
#             # return contracts, "Contratos obtenidos exitosamente"
#             contracts = db.session.query(Contract).from_statement(
#             text("SELECT * FROM contract_sumary")
#         ).all()
#             return contracts, "Contratos obtenidos exitosamente"
#         except Exception as e:
#             from app.logger import logger
#             logger.error(f"Error al obtener contratos: {str(e)}")
#             return [], "Error al obtener contratos"

# app/models/contract_summary.py
from app import db
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, DECIMAL
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from sqlalchemy import event
import json

class ContractSummary(db.Model):
    __tablename__ = 'contract_sumary'

    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    father_lastname = Column(String(255))
    mother_lastname = Column(String(255))
    client_name = Column(String(255))
    product_name = Column(String(255))
    contract_type_desc = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    status_desc = Column(String(100))
    total_price = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def get_all():
        json_results = []
        try:
            result = db.session.execute(text("SELECT * FROM contract_sumary")).all()
            if result:            
                for row in result:
                    print(row)
                    json_results.append(row._asdict())
                    # row_dict = {column.name: getattr(row, column.name) for column in row.__table__.columns}
                    # json_object = json.dumps(row_dict)
                    # json_results.append(json_object)
                return json_results, "Contratos obtenidos exitosamente"
            else:
                return [], "No se encontraron contratos"
            # if contracts:
            #     for contract in contracts:
            #         print(contract)
           
            # return contracts, "Contratos obtenidos exitosamente"
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener contratos: {str(e)}")
            return [], "Error al obtener contratos"
        
# --- Evitar INSERT, UPDATE y DELETE en la vista ---
@event.listens_for(ContractSummary, "before_insert")
@event.listens_for(ContractSummary, "before_update")
@event.listens_for(ContractSummary, "before_delete")
def readonly_operations(mapper, connection, target):
    raise SQLAlchemyError(f"La vista '{ContractSummary.__tablename__}' es de solo lectura")