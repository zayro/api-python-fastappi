# Instalacion

- pip install -r requirements.txt

- pip install pip-upgrader

- docker pull couchdb:3.3.3

## Enviroment

- python -m venv .venv
- .venv\Scripts\activate.bat
- pip install -r requirements.txt
- python.exe -m pip install --upgrade pip
- 'linux' source bin/activate
- 'windows' Scripts\activate.bat - .venv\Scripts\activate.bat

## Version

- python -V: 3.10.6

### Commands PIP

- pip install virtualenv
- pip install
- pip list
- pip install --upgrade fastapi

## Launch App

- uvicorn main:app
- uvicorn main:app --reload
- uvicorn main:app --reload --host 0.0.0.0 --port 4000
- uvicorn main:app --host 0.0.0.0 --port 4000
- uvicorn main:app --host 0.0.0.0 --port 4000 --workers 4

## Update

- pip install --upgrade fastapi

## Show Version

- pip show fastapi

## Services

- <http://localhost:5984/_utils/#login>

### Bibliografia

- Documentation FastAPI: <https://fastapi.tiangolo.com/>
- Documentar Websocket: <https://fastapi.tiangolo.com/tutorial/websockets/>
- Documentar JWT: <https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>
- Documentar CORS: <https://fastapi.tiangolo.com/tutorial/cors/>
- Documentar API: <https://documenter.getpostman.com/view/473681/2sB2qah1ao#261202a3-efb4-4627-8193-57db99b14a49>

#### Cors

- <https://www.slingacademy.com/article/fastapi-allowing-requests-from-other-origins-cors/>

 