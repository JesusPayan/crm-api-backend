import pandas as pd
import logging
import traceback


def get_list_from_csv(file,required_columns):
    try:
            # leer el archivo CSV con pandas
            df = pd.read_csv(file)
            # validar que tenga las columnas necesarias 
            for col in required_columns:
                if col not in df.columns:
                    return None, f"El CSV no contiene la columna requerida: {col}"

            # convertir a lista de registros
            records = df[required_columns].values.tolist()
            if records:
                return records
            else:
                return None
    except Exception as e:
        logging.error(f"error al procesar el CSV{file}:\n{traceback.format_exc()}")
        return None
