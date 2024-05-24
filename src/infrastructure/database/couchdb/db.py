import couchdb


class CouchDBServer:
    def __init__(self):
        self.db = self.connect_to_couchdb()

    def connect_to_couchdb(self):
        try:
            couch = couchdb.Server("http://admin:zayro1989@localhost:5984/")
            if "developer" not in couch:
                couch.create("developer")
            db = couch["developer"]
            print(f"Conectado a CouchDB")
            return db
        except couchdb.ServerError as e:
            print(f"Error al conectar a CouchDB: {e}")

    def create_document(self, document: dict):
        try:
            print(f"create_document:  ", "\n")
            if "user" in document:
                result_search_documents = self.search_documents({"user": document.get("user")})
                print(f"result_search_documents {result_search_documents }", "\n")
                if result_search_documents is None:
                    print("El documento ya existe en la base de datos")
                    doc_id, doc_rev = self.db.save(document)
                    print(f"Documento creado con ID: {doc_id}, revision: {doc_rev}")
                    return doc_id
                else:
                    print("El documento ya existe en la base de datos")
                    return None
            else:
                return None
        except couchdb.ResourceConflict as e:
            print(f"Error al crear el documento: {e}")

    def update_document(self, search_document, updated_document):
        try:
            result_documents = self.search_document_index(search_document)
            if not result_documents:
                print("El documento no existe en la base de datos")
                return None
            doc = self.db[result_documents]
            for campo, valor in updated_document.items():
                print(f"Actualizando el campo {campo} con el valor {valor}")
                doc[campo] = valor
            doc_id, doc_rev = self.db.save(doc)
            print(f"Documento actualizado con ID: {doc_id}, revision: {doc_rev}")
        except couchdb.ResourceConflict as e:
            print(f"Error al actualizar el documento: {e}")

    def update_document_history(self, search_document, updated_document):
        try:
            result_documents = self.search_document_index(search_document)
            if result_documents is None:
                print("El documento no existe en la base de datos")
                return None
            doc = self.db[result_documents]
            print(doc["history"], "\n")
            doc["history"].append(updated_document)
            print(doc)
            doc_id, doc_rev = self.db.save(doc)
            print(f"Documento actualizado con ID: {doc_id}, revision: {doc_rev}")
        except couchdb.ResourceConflict as e:
            print(f"Error al actualizar el documento: {e}")

    def delete_document(self, doc_id):
        try:
            self.db.delete(self.db[doc_id])
            print(f"Documento eliminado con ID: {doc_id}")
        except couchdb.ResourceNotFound as e:
            print(f"Error al eliminar el documento: {e}")

    def search_documents(self, query: dict):
        try:
            consulta = {"selector": query}
            result = self.db.find(consulta)
            documents = [doc for doc in result]
            print(f" documents  find {len(documents)}", "\n")
            if len(documents) > 0:
                for doc in documents:
                    print(f"Documento encontrado id: {doc['_id']}")
                print("Return Documents", type(documents), "\n")
                return documents
            else:
                print("No se encontraron documentos en la base de datos")
                return None
        except (couchdb.ResourceConflict, couchdb.ServerError) as e:
            print(f"Error al realizar la búsqueda: {e}")

    def search_document_index(self, query: dict):
        try:
            consulta = {"selector": query}
            result = self.db.find(consulta)
            documents = [doc for doc in result]
            if len(documents) > 0:
                for doc in documents:
                    print(f"Documento encontrado id: {doc['_id']}")
                return doc["_id"]
            else:
                print("No se encontraron documentos en la base de datos")
                return None
        except (couchdb.ResourceConflict, couchdb.ServerError) as e:
            print(f"Error al realizar la búsqueda: {e}")


# Ejemplo de uso
""" 
couchdb = CouchDB()

user = {
    "user": "102030",
    "history": [
        {
            "module": "init session",
            "time_start": "2021-10-10 10:00:00",
        }
    ],
}
result_create_document = couchdb.create_document(user)
print(result_create_document)

query = {"user": "102030"}
# couchdb.search_documents(query)

update_data = {
    "module": "nuevi",
    "time_start": "2021-10-10 10:03:00",
}
# couchdb.update_document(query, update_data)
result_update_document_history = couchdb.update_document_history(query, update_data)
print(result_update_document_history)
"""
