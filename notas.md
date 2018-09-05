# Parte 1

La mejor forma de hacer aplicaciones grandes en Flask es usandola como un paquete de Python.

En Python, un subdirectorio que contiene un archivo **\___init.py__\_** se considera un paquete y se
puede importar. Cuando se importa un paquete, \___init.py__\_ ejecuta y define que simbolos expone el
paquete al mundo exterior.

Dentro de la carpeta 'microblog' se crea el paquete 'app' y dentro de este el archivo \___init.py__.

El script:

	from flask import Flask

	app = Flask(__name__)

Crea el objeto de la aplicación (app) como una instancia de la clase Flask importada desde el
paquete flask. La variable \___name__\_ es una variable predefinida por Python que se configura con
el nombre del modulo en el que se utiliza. Flask utiliza la ubicación de este modulo como punto de
partida cuando necesita cargar recursos asociados como: los templates.

En el ejemplo se explica que puede haber confusión es que hay dos entidades llamadas **app**:

1. El paquete **app** que es definido por la carpeta 'app' y el archivo \___init.py__\_.
2. Y es referenciada en sentencia: 'from app import routes'.

La variable _app_ se definió como una instancia de la clase Flask en el archivo \___init.py__\_ lo
que la hace miembro de paquete _app_.

Otra cosa a tener en cuenta en la importación del modulo 'routes' en la parte inferior y no al
inicio del archivo - como es costumbre -. Con esto se busca evitar el problema de la importaciones
circulares. Como el modulo _routes_ necesita importar la variable **app** definida en el archivo,
colocando una de las importaciones recíprocas al final evita el error que resulta de la referecias
entre estas.

> Módulo 'routes': el módulo rutas maneja las diferentes URL's de la aplicación.
En Flask loss manejadores de las rutas se escriben como funciones de Python llamadas **view functions**
o **funciones de vistas**. Las vistas (views) se asignan a una o más rutas (routes) para que Flask
sepa qué lógica ejecutar cuando un cliente solicita un URL.

> Para completar la aplicación hay que crear un script de Python en el nivel superior que defina la
instancia de la aplicación Flask. Es recomendable nombrar este archvio como el nombre del proyecto:

	microblog.py

	microblog/
		venv/
		app/
			____init.py__
			routes.py
		microblog.py

Definimos este archivo con un 'import' de la instancia de la aplicación.

	from app import app

Recuerda que habian 2 entidades **app**, allí se pueden ver juntas. La instancia de la aplicación
Flask llamada _app_ que es miembro del paquete _app_. Si esto es confuso es posible renombrar la
variable o el paquete.

##### Ejecutar aplicación Flask

Para ejecutar una aplicación primero hay que configurar la variable de entorno **FLASK_APP**

	(venv) $ export FLASK_APP=microblog.py

Luego correr la aplicación:

	(venv) $ flask run

El manejo de variables de entorno para el caso de Flask es un poco engorroso ya que al cerrar la
terminal estas son eliminadas. Para configurar las varibles de forma automatica:

Instalar:

	(venv) $ pip install python-dotenv

Crear un archivo _.flaskenv_ en el nivel superior y dentro de este configurar la varibles de entorno

	FLASK_APP = microblog.py

Cualquiera de las dos formas es valida.