# Arquitecta Limpia

## Dominio

El dominio es el corazon de una aplicación y tiene que estar totalmente aislado de cualquier dependencia ajena a la lógica o los datos de negocio. El dominio es independiente de cualquier framework o librería y puede ser reutilizado en cualquier aplicación.

**Entidades**: Son los objetos de negocio que representan el dominio de la aplicación, ejemplos de entidades son: `Usuario`, `Producto`, `Venta`, `Compra`. la nombratura de las entidades debe ser en singular, ejemplo: `UsuarioEntity`, `ProductoEntity`, `VentaEntity`, `CompraEntity`.

un ejemplo de codigo de una entidad seria:

```python
class UsuarioEntity:
    def __init__(self, id: int, nombre: str, email: str, password: str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
```

**Repositorios**: Son los encargados de la persistencia de los datos, ejemplos de repositorios son: `Usuario`, `Producto`, `Venta`, `Compra`
. la nombratura de los repositorios debe ser en singular, ejemplo: `UsuarioRepository`, `ProductoRepository`, `VentaRepository`, `CompraRepository`.

un ejemplo de codigo de un repositorio seria:

```python
class UsuarioRepository:
    def __init__(self, driver):
        self.driver = driver

    def crear(self, usuario: UsuarioEntity):
        pass

    def eliminar(self, id: int):
        pass

    def actualizar(self, usuario: UsuarioEntity):
        pass

    def listar(self):
        pass

```

**Modelos**: Son los encargados de representar los datos de la aplicación, ejemplos de modelos son: `UsuarioModel`, `ProductoModel`, `VentaModel`, `CompraModel`.

un ejemplo de codigo de un modelo seria:

```python
class UsuarioModel:
    def __init__(self, id: int, nombre: str, email: str, password: str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

```

los modelos y las entidades son similares, pero los modelos son los encargados de representar los datos de la aplicación, mientras que las entidades son los objetos de negocio que representan el dominio de la aplicación.

## Casos de Uso o Aplicación

Los casos de uso son las acciones que se pueden realizar en la aplicación, cada caso de uso tiene una única responsabilidad y se encarga de una sola acción. Los casos de uso son independientes de cualquier framework o librería y pueden ser reutilizados en cualquier aplicación.

**Interactores**: Son los encargados de la lógica de negocio de la aplicación, ejemplos de interactores son: `CrearUsuario`, `EliminarUsuario`, `ActualizarUsuario`, `ListarUsuarios`. los interactores tambien reciben los nombres de caso de uso y usan una nomenclatura al crear el archivo.

ejemplo de codigo de un interactores seria:

```python
class CrearUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, usuario: UsuarioEntity):
        pass

```

**Controladores**: Son los encargados de recibir las peticiones HTTP, llamar a los interactores y devolver una respuesta HTTP, ejemplos de controladores son: `UsuarioController`, `ProductoController`, `VentaController`, `CompraController`.

ejemplo de codigo de un controlador seria:

```python
class UsuarioController:
    def __init__(self, crear_usuario):
        self.crear_usuario = crear_usuario

    def crear(self, request):
        pass


```

### Reglas de Negocio

**Validaciones**: Son las reglas que se deben cumplir para que una entidad sea válida, ejemplos de validaciones son: `El email debe ser único`, `La contraseña debe tener al menos 8 caracteres`, `El nombre no puede estar vacío`.

**Excepciones**: Son los errores que se pueden producir en la aplicación, ejemplos de excepciones son: `UsuarioNoEncontrado`, `ProductoNoEncontrado`, `VentaNoEncontrada`, `CompraNoEncontrada`.

**Casos de Uso**: Son los casos de uso de la aplicación, ejemplos de casos de uso son: `CrearUsuario`, `EliminarUsuario`, `ActualizarUsuario`, `ListarUsuarios`. se usan para definir las acciones que se pueden realizar en la aplicación y contienen la lógica de negocio.

un ejemplo de codigo de un caso de uso seria:

```python
class CrearUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, usuario: UsuarioEntity):
        pass


```

**Servicios**: Son los servicios que se pueden consumir en la aplicación, ejemplos de servicios son: `EnviarEmail`, `EnviarSMS`, `EnviarNotificación`.

**Eventos**: Son los eventos que se pueden producir en la aplicación, ejemplos de eventos son: `UsuarioCreado`, `UsuarioEliminado`, `UsuarioActualizado`, `UsuarioListado`.

**Notificaciones**: Son las notificaciones que se pueden enviar en la aplicación, ejemplos de notificaciones son: `EmailEnviado`, `SMSEnviado`, `NotificaciónEnviada`.

**Middlewares**: Son funciones que se ejecutan antes de llegar a los controladores, ejemplos de middlewares son: `authMiddleware`, `adminMiddleware`, `loggerMiddleware`.

**Serializadores**: Son los encargados de transformar los datos de la aplicación a un formato específico, ejemplos de serializadores son: `UsuarioSerializer`, `ProductoSerializer`, `VentaSerializer`, `CompraSerializer`.

## Infraestructura

son los elementos externos con los que se comunica la aplicación, tanto de entrada como de salida, como bases de datos, servicios, APIs, etc. La infraestructura es independiente de cualquier framework o librería y puede ser reutilizada en cualquier aplicación.

**Adaptadores**: Son los encargados de adaptar la aplicación a un framework o librería con fastApi, ejemplos de adaptadores son: `RepositorioUsuariosPostgresql`, `CacheUsuariosRedis`, `ControladorMensajesRabbitMQ`.

**entry-point**: Es el punto de entrada de la aplicación, ejemplos de entry-point son: `index`, `app`.

**Rutas**: Son los encargados de definir las rutas de la aplicación, ejemplos de rutas son: `GET /usuarios`, `POST /usuarios`, `PUT /usuarios`, `DELETE /usuarios`, se usan en la capa de infraestructura especificamente en el entry-point.

**config**: Son los archivos de configuración de la aplicación, ejemplos de configuraciones son: `database`, `email`, `sms`.

**helpers**: Son funciones de ayuda que se pueden reutilizar en la aplicación, ejemplos de helpers son: `validarEmail`, `validarPassword`.

## Ejemplo

project_backend/
├── src/
│   ├── application/
│   │   ├── controllers.py
│   │   ├── usecases/
│   │   │   ├── crear_usuario.py
│   │   │   └── actualizar_usuario.py
│   ├── domain/
│   │   ├── entities.py
│   │   ├── value_objects.py
│   ├── infrastructure/
│   │   ├── adapters/
│   │   │   ├── repositorio_usuarios_postgresql.py
│   │   │   ├── cache_usuarios_redis.py
│   │   │   └── controlador_mensajes_rabbitmq.py
│   │   ├── drivers/
│   │   │   ├── postgresql_driver.py
│   │   │   └── redis_driver.py
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── controladores.py
│   │   │   └── rutas.py
│   └── main.py
├── requirements.txt
├── README.md
└── tests/
    ├── application/
    │   ├── test_controllers.py
    │   └── test_usecases.py
    ├── domain/
    │   └── test_entities.py
    └── infrastructure/
        └── test_adapters.py

### Bibliografia

#### Arquitectura limpia

* <https://www.linkedin.com/pulse/clean-architecture-en-node-y-express-odannys-de-la-cruz/>

* <https://www.adictosaltrabajo.com/2019/07/02/capas-cebollas-y-colmenas-arquitecturas-en-el-backend/>

* <https://www.paradigmadigital.com/dev/patrones-arquitectura-microservicios-que-son-ventajas/>

* <https://www.mytaskpanel.com/las-5-ventajas-que-debes-saber-sobre-utilizar-una-clean-architecture/>

* <https://www.genbeta.com/desarrollo/principios-de-una-arquitectura-limpia-mantenible-y-testeable>

#### Codigo Limpio

* <https://github.com/andersontr15/clean-code-javascript-es>
