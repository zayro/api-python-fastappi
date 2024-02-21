# Instalacion

- pip install -r requirements.txt

### Update Package

- pip install pip-upgrader

## Enviroment

- virtualenv api
- cd api
- 'linux' source bin/activate
- 'windows' Scripts\activate.bat

## Version

- python -V

### Commands PIP

- pip install
- pip list

## Launch App

- uvicorn main:app
- uvicorn main:app --reload
- uvicorn main:app --reload --host 0.0.0.0 --port 4001
- uvicorn main:app --host 0.0.0.0 --port 4001
- uvicorn main:app --host 0.0.0.0 --port 4001 --workers 4

## Show Version

- pip show fastapi

### Bibliografia

- <https://www.slingacademy.com/article/fastapi-allowing-requests-from-other-origins-cors/>
