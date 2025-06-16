# bot-mareas
Una vez al día pilla las mareas de TF a un fichero. Un bot de telegram sirve esta info cuando es consultado.


crear EV dentro del proyecto
python -m venv venv

activar EV:
venv\Scripts\activate


Dependencias:
pip install -r requirements.txt



para que visual studio pille el python del Entorno Virtual:
CTRL + Mayus + p : Python: Select Interpreter


------------------------------------- Despliegue en linux:

En windows creo el siguiente fichero de requerimientos
pip freeze > requirements.txt

Ahora en linux una vez clonado el proyecto ejecuto:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
