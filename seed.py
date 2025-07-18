from app import create_app, db
from app.models import Client, Product, Contract, Catalog, CatalogValue
from datetime import datetime, date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

# Crear clientes
    client1 = Client(
        name="Juan",
        father_lastname="Pérez",
        mother_lastname="García",
        telephone1="6691234567",
        email1="juan.perez@mail.com",
        status=1,
        status_desc="Activo",
        created_by="seed",
        created_at=datetime.now()
    )

    client2 = Client(
        name="Ana",
        father_lastname="López",
        mother_lastname="Martínez",
        telephone1="6699876543",
        email1="ana.lopez@mail.com",
        status=1,
        status_desc="Activo",
        created_by="seed",
        created_at=datetime.now()
    )

    # Crear productos
    product1 = Product(
        cve_internal="PROD-001",
        description="Cámara de seguridad",
        price=1499.99,
        image="https://via.placeholder.com/150",
        status=1,
        status_desc="Disponible",
        created_by="seed",
        created_at=datetime.now()
    )

    product2 = Product(
        cve_internal="PROD-002",
        description="Router WiFi",
        price=899.50,
        image="https://via.placeholder.com/150",
        status=1,
        status_desc="Disponible",
        created_by="seed",
        created_at=datetime.now()
    )

    # Crear contratos
    contract1 = Contract(
        client=client1,
        product=product1,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status=1,
        status_desc="Vigente",
        created_by="seed",
        created_at=datetime.now()
    )

    # Crear catálogo
    catalog = Catalog(
        cve_table="STATUS_CLIENT",
        desc_table="Estados del cliente",
        status=1,
        status_desc="Activo",
        created_by="seed",
        created_at=datetime.now()
    )

    # Crear valores del catálogo
    val1 = CatalogValue(
        catalog=catalog,
        sequence_id=1,
        key01="1",
        value01="Activo",
        status=1,
        status_desc="Activo",
        created_by="seed",
        created_at=datetime.now()
    )

    val2 = CatalogValue(
        catalog=catalog,
        sequence_id=2,
        key01="0",
        value01="Inactivo",
        status=1,
        status_desc="Activo",
        created_by="seed",
        created_at=datetime.now()
    )

    db.session.add_all([client1, client2, product1, product2, contract1, catalog, val1, val2])
    db.session.commit()
    db.session.commit()
    print("✅ Datos de prueba insertados")

    db.session.close()