from app import db
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, DECIMAL
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from sqlalchemy import event
import json

class ClientSummary(db.Model):
    __tablename__ = 'client_sumary'

    id = Column(Integer, primary_key=True)
    cve_internal = Column(String(50))
    client_name = Column(String(255))
    client_father_lastname = Column(String(100))
    client_mother_lastname = Column(String(100))
    telephone1 = Column(String(20))
    email1 = Column(String(100))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def get_all():
        json_results = []
        try:
            result = db.session.execute(text("select * from client_summary")).all()
            if result:            
                for row in result:
                    print(row)
                    json_results.append(row._asdict())
                    # row_dict = {column.name: getattr(row, column.name) for column in row.__table__.columns}
                    # json_object = json.dumps(row_dict)
                    # json_results.append(json_object)
                return json_results, "Clientes obtenidos exitosamente"
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
@event.listens_for(ClientSummary, "before_insert")
@event.listens_for(ClientSummary, "before_update")
@event.listens_for(ClientSummary, "before_delete")
def readonly_operations(mapper, connection, target):
    raise SQLAlchemyError(f"La vista '{ClientSummary.__tablename__}' es de solo lectura")