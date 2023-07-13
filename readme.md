# Instalacion

- pip install -r requirements.txt

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
