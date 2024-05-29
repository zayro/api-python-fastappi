import sys
import psycopg2
from typing import List, Optional

from pydantic import ValidationError
from src.core.config import settings
from src.domain.entity.user_entity import User, UserLogin, UserPasswordChange
from src.infrastructure.log.logService import ic


class UserRepository:
    """Implementación concreta de un repositorio de usuarios utilizando una base de datos PostgreSQL."""

    def _connect(self):
        """Connect to the PostgreSQL database server"""
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(dsn=settings.DATABASE_URL) as conn:
                print("Connected to the PostgreSQL server.")
                # Cierra el cursor (no necesario dentro del context manager)
                # cur.close()

                return conn
            # La conexión se cierra automáticamente al salir del bloque `with`
        except (Exception, psycopg2.DatabaseError, TypeError) as e:
            print("----- Exception General Database ----- ")
            print(
                type(e).__name__,  # TypeError
                __file__,  # /tmp/example.py
                e.__traceback__.tb_lineno,  # 2
            )
            print(str(e))
            print("---------- ")
            sys.exit()
            # muestra si existen errores
        finally:
            # Cierra el cursor (no necesario dentro del context manager)
            # cur.close()

            # Verifica si la conexión se cerró correctamente
            if conn is not None and conn.closed != 1:
                print("Conexion cerrada exitosamente")
            else:
                print("Error al cerrar la conexion")

    def _execute_query(self, query: str, values: tuple = None):
        """Método auxiliar para ejecutar consultas SQL con un gestor de contexto."""
        try:
            with self._connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, values)
                    result = None
                    if cursor.description:  # Verifica si la consulta tiene resultados
                        result = cursor.fetchall()
                    connection.commit()
                    return result
        except (psycopg2.DatabaseError, TypeError) as e:
            print("----- Exception General Database ----- ")
            print(str(e))
            print("---------- ")

            # muestra si existen errores
        finally:

            # Verifica si la conexión se cerró correctamente
            if connection is not None and connection.closed != 1:
                print("Conexion cerrada exitosamente")
            else:
                print("Error al cerrar la conexion")

    def create(self, user: User) -> User:
        """Crea un nuevo usuario en la base de datos."""
        query = """
        INSERT INTO users (username, email, full_name)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, full_name;
        """
        values = (user.username, user.email, user.full_name)
        result = self._execute_query(query, values)
        if result:
            user_id, username, email, full_name = result[0]
            return User(id=user_id, username=username, email=email, full_name=full_name)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID de la base de datos."""
        query = """
        SELECT id_users, username, email
        FROM users
        WHERE id_users = %s;
        """
        values = (user_id,)
        result = self._execute_query(query, values)
        if result:
            id_users, username, email = result[0]
            return User(id_users=id_users, username=username, email=email)
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su nombre de usuario de la base de datos."""

        try:
            query = """
            SELECT id_users, username, email, password
            FROM auth.view_privileges
            WHERE username = %s;
            """
            values = (username,)
            result = self._execute_query(query, values)
            if result:
                print(result)
                id_users, username, email, password = result[0]
                return User(id_users=id_users, username=username, email=email, password=password)
            return None
        except (ValidationError, TypeError) as e:
            print("----- Exception General Database ----- ")
            print(str(e))

    def get_all(self) -> List[User]:
        """Obtiene todos los usuarios de la base de datos."""
        try:
            query = """
            SELECT id_users, username, email, password
            FROM auth.users;
            """
            result = self._execute_query(query)
            users = []
            for row in result:
                id_users, username, email, password = row
                user = User(id_users=id_users, username=username, email=email, password=password)
                users.append(user)
            return users
        except (ValidationError, TypeError) as e:
            print("----- Exception General Database ----- ")
            print(str(e))

    def update(self, user: User) -> Optional[User]:
        """Actualiza un usuario existente en la base de datos."""
        query = """
        UPDATE users
        SET username = %s, email = %s, full_name = %s
        WHERE id = %s
        RETURNING id, username, email, full_name;
        """
        values = (user.username, user.email, user.full_name, user.id)
        result = self._execute_query(query, values)
        if result:
            id, username, email, full_name = result[0]
            return User(id=id, username=username, email=email, full_name=full_name)
        return None

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID de la base de datos."""
        query = """
        DELETE FROM users
        WHERE id = %s;
        """
        values = (user_id,)
        self._execute_query(query, values)
        return True

    def auth_user(self, login: UserLogin) -> dict:
        """Execute Sql Postgresql"""
        ic(login)
        sql = """ SELECT email, username, password FROM auth.users WHERE username = %s """
        return self._execute_query(sql, (login.username))

    def update_password_user(self, data: UserPasswordChange) -> dict:

        sql = """ UPDATE auth.users SET password = %(newPassword)s  WHERE email = %(email)s  RETURNING email, username """

        values = (data.newPassword, data.email)

        return self._execute_query(sql, values)

    def create_user_trasaction(self, payload_user: dict) -> dict:
        """Execute Sql Postgresql"""

        try:
            with self._connect() as conn:

                conn.autocommit = False

                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                    sql_max_id_field_user = """SELECT MAX(id_users) + 1 as id_users FROM auth.users """

                    cur.execute(sql_max_id_field_user)

                    execute_max_id_field_user = cur.fetchone()

                    ic(payload_user)

                    payload_user.update(execute_max_id_field_user)

                    sql_insert_user = (
                        """INSERT INTO auth.users (id_users, username, password, email) VALUES (%(id_users)s, %(username)s, %(password)s, %(email)s) RETURNING id_users"""
                    )

                    cur.execute(sql_insert_user, payload_user)

                    execute_insert_user = cur.fetchone()[0]

                    ## second query

                    sql_max_id_field_users_validation = """SELECT MAX(id_users_validation) + 1 as id_users_validation FROM auth.users_validation """

                    cur.execute(sql_max_id_field_users_validation)

                    payload_user_validation = {
                        "id_users_roles": 2,
                        "status": 1,
                        "verified": False,
                    }

                    execute_max_id_field_user_validation = cur.fetchone()

                    payload_user_validation.update(execute_insert_user)

                    payload_user_validation.update(execute_max_id_field_user_validation)

                    sql_insert_user_validation = """INSERT INTO auth.users_validation (id_users_validation, id_users_roles, id_users, status, verified) VALUES (%(id_users_validation)s, %(id_users_roles)s, %(id_users)s, %(status)s, %(verified)s) RETURNING id_users_validation"""

                    cur.execute(sql_insert_user_validation, payload_user_validation)

                    conn.commit()
                    ic("Transaction completed successfully create user ")

                    response_to_controller: dict = {
                        "success": True,
                        "message": "se ejecuto Exitosamente",
                    }

                    return response_to_controller

        except (psycopg2.DatabaseError, ValidationError) as error:
            ic(error)
            conn.rollback()
            return {
                "success": False,
                "message": "Error al ejecutar la consulta",
                "error": str(error),
            }
