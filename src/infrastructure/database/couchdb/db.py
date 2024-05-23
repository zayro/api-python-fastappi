import couchdb


# Establecer la conexión con la base de datos CouchDB
def connect_to_couchdb():
    try:
        # Especifica la URL del servidor CouchDB
        couch = couchdb.Server("http://localhost:5984/")

        # Verifica si la base de datos existe, si no, la crea
        if "mydatabase" not in couch:
            couch.create("mydatabase")

        # Conecta a la base de datos
        db = couch["mydatabase"]

        # Retorna la conexión a la base de datos
        return db

    except couchdb.ServerError as e:
        print(f"Error al conectar a CouchDB: {e}")


# Ejemplo de uso
db = connect_to_couchdb()
if db:
    print("Conexión exitosa a CouchDB")


# Establecer la conexión con la base de datos CouchDB
def create_document(db, document):
    try:
        # Crea un nuevo documento en la base de datos
        doc_id, doc_rev = db.save(document)
        print(f"Documento creado con ID: {doc_id}")
        return doc_id
    except couchdb.ResourceConflict as e:
        print(f"Error al crear el documento: {e}")


def read_document(db, doc_id):
    try:
        # Obtiene un documento de la base de datos por su ID
        document = db[doc_id]
        print(f"Documento encontrado: {document}")
        return document
    except couchdb.ResourceNotFound as e:
        print(f"Error al leer el documento: {e}")


def update_document(db, doc_id, updated_document):
    try:
        # Actualiza un documento existente en la base de datos
        updated_document["_id"] = doc_id
        updated_document["_rev"] = db[doc_id]["_rev"]
        db.save(updated_document)
        print(f"Documento actualizado con ID: {doc_id}")
    except couchdb.ResourceConflict as e:
        print(f"Error al actualizar el documento: {e}")


def delete_document(db, doc_id):
    try:
        # Elimina un documento de la base de datos por su ID
        db.delete(db[doc_id])
        print(f"Documento eliminado con ID: {doc_id}")
    except couchdb.ResourceNotFound as e:
        print(f"Error al eliminar el documento: {e}")


# Ejemplo de uso
db = connect_to_couchdb()
if db:
    # Crear un nuevo documento
    document = {"name": "John Doe", "age": 30}
    doc_id = create_document(db, document)

    # Leer el documento creado
    read_document(db, doc_id)

    # Actualizar el documento creado
    updated_document = {"name": "John Smith", "age": 35}
    update_document(db, doc_id, updated_document)

    # Leer el documento actualizado
    read_document(db, doc_id)

    # Eliminar el documento
    delete_document(db, doc_id)
