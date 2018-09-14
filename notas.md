# Parte 1 (Hello, World)

La mejor forma de hacer aplicaciones grandes en Flask es usandola como un paquete de Python.

En Python, un subdirectorio que contiene un archivo **\___init.py__\_** se considera un paquete y se
puede importar. Cuando se importa un paquete: \___init.py__\_ ejecuta y define que simbolos expone el
paquete al mundo exterior.

Dentro de la carpeta 'microblog' se crea el paquete 'app' y dentro de este el archivo \___init.py__.

El script:

	from flask import Flask

	app = Flask(__name__)

Crea el objeto de la aplicación (app) como una instancia de la clase Flask importada desde el
paquete flask. La variable \___name__\_ es una variable predefinida por Python que se configura con
el nombre del modulo en el que se utiliza. Flask utiliza la ubicación de este modulo como punto de
partida cuando necesita cargar recursos asociados como: los templates.

En el ejemplo se explica que puede haber confusión ya que hay dos entidades llamadas **app**:

1. El paquete **app** que es definido por la carpeta 'app' y el archivo \___init.py__\_.
2. Y es referenciada en la sentencia: 'from app import routes'.

La variable _app_ se definió como una instancia de la clase Flask en el archivo \___init.py__\_ lo
que la hace miembro de paquete _app_.

Otra cosa a tener en cuenta es la importación del modulo 'routes' en la parte inferior y no al
inicio del archivo - como es costumbre -. Con esto se busca evitar el problema de la importaciones
circulares. Como el modulo _routes_ necesita importar la variable **app** definida en el archivo,
colocando una de las importaciones recíprocas al final evita el error que resulta de la referencias
circulares.

-- Para aprender mas de referencias circulares: https://stackabuse.com/python-circular-imports/

> Módulo 'routes': el módulo rutas maneja las diferentes URL's de la aplicación.
En Flask los manejadores de las rutas se escriben como funciones de Python llamadas **view functions**
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

### Ejecutar aplicación Flask

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


# Parte 2 (Templates)

### ¿Que son los templates?

Los templates ayudan a mantener separados la presentación y la logica del negocio. Los templates
se crean en archivos separados y se guardan en una carpeta llamada "templates" que está
dentro del paquete de la aplicación:

	microblog/
		app/
			templates/

> La operación de convertir un template en una página HTML completa se llama _rendering_ (renderizar).
Para renderizar un template se usa la función **render_template()** que viene dentro de Flask.


# Parte 3 (Web Forms)

### Introducción a Flask-WTF

Para manejar los formularios web en esta aplicación se va a usar la extensión **Flask-WTF**

Instalar Flask-WTF:

	(venv) $ pip install flask-wtf

### Configuración

La mejor manera de mantener las configuraciones (hay varias) es utilizando clases. Estas clases
estarán en modulo de python _config.py_ en el nivel más alto del proyecto.

	import os

	class Config(object):
    	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

Las configuraciones son definidas como variables de clase dentro de la clase _Config_, a medida
que se necesiten más configuraciones se pueden añadir a esta clase. Si se llegasen ha necesitar más
de un conjunto de configuraciones se pueden crear subclases a partir de esta; por ejemplo diferentes
configuraciones para diferentes ambientes: Desarrollo, Producción, etc.

La variable **SECRET_KEY** es la unica que no puede faltar en ninguna aplicación Flask ya que por
medio de sta algunas extensiones de Flask generan _tokens_ encriptados y permite la protección 
contra ataques CSRF.

**En el ambiente de producción es vital mantener esta llave fuera del alcance**

Despues de tener la configuración lista debo decirle al Flask que la lea y la aplique. Esto se puede
despues de instanciar la aplicación de Flask con el método: **app.config.from_object()**

Los items de la configuración pueden ser accedidas mediante la sintaxis de un diccionario desde:
**app.config**.

	>>> from microblog import app
	>>> app.config['SECRET_KEY']
	'your secret key'

### User Login Form

La extensión **Flask-WTF** usa clases de Python para reprensentar formularios web. Una clase
simplemente define los campos del formulario como variables de clase.

Las definiciones de los formularios van en el modulo **forms.py** dentro del paquete _app_.

### Form Templates

Una vez definidos los Formularios, hay que añadirlos a un template HTML para que estos sean
renderizados en la página web. La ventaja de usar de esta manera los formularios, es que
ellos se renderizan automaticamente en formato HTML.

Ver:
	app/templates/login.html

### Form Views

El paso final para poder ver el formulario en la web es crear una vista que renderize el formulario
que se creo en el paso anterior.

Ver:
	app/routes.py 
	-- login()


### Receiving Form Data

El método **form.validate_on_submit()** hace que todo el procesamiento de formularios funcione.
Cuando el navedador envía un request _GET_ para recibir la página con el formulario, este método
retorna _False_, por lo que la función omite la instrucción _if_ y va directamente a renderizar 
el HTML.

La función **flash()** es una forma útil de mostrar un mensaje al usuario. Muchas aplicaciones
usan esta técnica para informar al usuario si alguna acción ha sido exitosa o no. En este caso,
se usa mecanismo como una solución temporal, porque aún no se tiene toda la infraestructura
necesaria para registrar usuarios reales.

Cuando se invoca la función **flash()**, Flask almacena el mensaje pero esté no aparece magicamente
en la página web. Los templates de la aplicación necesitan renderizar estos mensajes de una forma
que funcione para el diseño del sitio. Lo mejor es añadir estos mensajes al template base (base.html)

Con el uso del constructor **with** el resultado de llamar al método **get_flashed_messages()** y
se le asigna a la varible **message**. La función **get_flashed_messages** viene con Flask y retorna
una lista de todos los mensajes que han sido registrados previamente con **flash()**.

Una propiedad interesante de estos mensajes es que una vez que se solicitan través de la función
**get_flashed_messages**, se eliminan de la lista de mensajes, por lo que aparecen una sola vez
después de llamar a la función **flash()**.


### Improving Field Validation (Mejorando las validaciones de los campos)

En el archivo **login.html** se agregan ciclos for después de los input de username y password
estos van a mostrar los mensajes de error enviados por los validadores.

Por regla general cualquier campo que tenga un validador tendra atado un mensaje de error de la
forma **form.<field name>.errors**


### Generating Links (Generando links)

Un problema de escribir los links directamente en los templates o en los archivo fuente es que si
un día se decide reorganizar todos los links, se tendran que buscar por toda la aplicación.

Para tener un mejor control de los links, Flask provee la función **url_for()** la cual genera URLs
usando un mapeador interno de funciones de vistas. 
	
	Ejemplo:

		url_for('login')  // Retorna '/login'

El argumento de url_for() es el nombre del _endpoint_, que en este caso es el nombre de la función
de vista.


# Parte 4 (Database)

### Databases in Flask

El autor da un consejo acerca de cuando usar bases de datos SQL y noSQL: Dice que es mejor usar
bases de datos SQL cuando la aplicación va a manejar datos estructurados como: listas de usuarios,
blogs, etc., y noSQL cuando la aplicación maneja datos menos definidos.

En Flask se recomienda el uso de la extención **Flask-SQLAlchemy** que proporciona un contenedor
(wrapper) compatible con Flask del paquete **SQLAlchemy** que es un ORM (Object Relational Mapper).

Los ORMs permites a las aplicaciones manejar las bases de datos usando entidades de alto nivel como
clases, objetos y métodos, en lugar de tablas y SQL. El trabajo del ORM es traducir las operaciones
de alto nivel en comandos de base de datos.

Una ventaja de SQLAlchemy es que no es un ORM de solo una base de datos sino que funciona con varias
bases de datos relacionales (MySQL, PostgreSQL, SQLite). 

Para instalar Flask-SQLAlchemy:

	(venv)$ pip install flask-sqlalchemy 

### Database Migrations

La extensión **Flask_Migrate** es un contenedor de Flask para **Alembic** que es un framework de
migración de bases de datos para SQLAlchemy.

Instalación:

	(venv)$ pip install flask-migrate

### Flask-SQLAlchemy Configuration

-- En este unto del tutorial se va a usar SQLite.

*Ver config.py clase Config()*

