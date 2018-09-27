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

-- En este punto del tutorial se va a usar SQLite.

*Ver config.py clase Config()*

**Flask-SQLAlchemy** toma la ubicación de la base de datos de la variable **SQLALCHEMY_DATABASE_URI**
En general es buena práctica establecer las configuraciones a partir de variables de entorno y
proporcionar un valor de retorno cuando el entorno no define la variable. En el caso del ejemplo
se toma la URL de la base de datos desde la variable de entorno _DATABASE_URL_, si la variable de 
entorno no está, se configura una base de datos llama _app.db_ localizada en el directorio principal
de la aplicación que está ubicada en la variable _basedir_.

La variable **SQLALCHEMY_TRACK_MODIFICATIONS** se establece en False para deshabilitar la opción de
Flask-SQLAlchemy de enviar una señal a la aplicación cada vez que se hacen cambios en la base de
datos.

La base de datos se va a representar con una _instancia_ de la BD, el motor de migración de la BD
tambien tendrá una instancia. Estos objetos serán creados despues de la aplicación en el archivo:
**app/__init__.py**.

### Database Models

La información que se almacenará en la BD se reprensetaran por una colección de clases, generalmente
llamadas modelos de bases de datos. El ORM se SQLAlchemy hará las traducciones necesarias para
asignar los objetos creados a partir de estas clases en filas y tablas.

Los modelos se crean en el modulo **app/models.py**.

Todos los models debe heradar de **db.Model** que es una clase base de Flask-SQLAlchemy.
La clase **User** define los campos como variables de clase. Los campos son instancias de **db.Column**
que toma como argumento el tipo del campo, ademas de otros argumentos opcionales.

### Creating The Migration Repository

**Alembic** (el framework de migración usado por Flask-Migrate) mantiene un repositorio de migración,
en el que almacena sus scripts de migración. Cada vez que se realiza un cambio en el esquema de la
base de datos, se agrega un script de migración al repositorio con los detalles del cambio. Para
aplicar las migraciones, estos scripts se ejecutan en la secuencia en que fueron creados.

Flask-Migrate expone sus comandos atravez del comando **flask** (como flask run). Pero para este
caso es **flask db**, este subcomando controla todo lo relacionado con las migraciones de las
bases de datos.

> Para crear el repositorio para las migraciones:

	(venv)$ flask db init

### The First Database Migration

Para crear una migración: **flask db migrate**

	(venv) $ flask db migrate -m "users table"

El comando anterior solo genera el script para crear las tablas, para aplicar las migraciones:

	(venv) $ flask db upgrade

### Database Upgrade and Downgrade Workflow

Suponiendo que tenemos una aplicación en dos ambientes, desarrollo y producción, y que necesitamos
crear campos o tablas nuevas, lo que debemos hacer es crear los cambios, generar el script de
migración ($ flask db migrate), y probar los cambios en desarrollo ($ flask db upgrade), una vez
confirmado que todo sale bien, se puede añadir el script a git y hacer un commit de este a
producción. Luego en producción aplicar los cambios ($ flask db upgrade).

Con **flask db downgrade** se pueden deshacer los ultimos cambios hechos en la BD.

### Database Relationships

La clase _User_ tiene un nuevo campo **post**, que es inicializado con **db.relationship**. Este no
es un campo, sino una vista de alto nivel para las relaciones entre _users_ y _post_.

Para las relaciones uno-a-muchos **db.relationship** se declara en el campo de 'uno' y es usado como
una forma conveniente para obtener acceso a 'muchos'. El primer argumento de _db.relationship_ es la
clase que representa el model de 'muchos'. Este argumento se puede proveer como un string con el
nombre de la clase si el modelo esta definido más adelante en el modulo.

El argumento **backref** define el nombre que se va a añadir a los objectos de 'muchos'. Esto añade una
expresión **post.author** que retorna el nombre del usuario que escribió el post.

### Play Time

Para trabajar con los models hay que entrar al intrepete de Python.

	>>> from app import db
	>>> from app.models import User, Post

> Para crear un nuevo usuario:
	
	>>> u = User(username='john', email='john@example.com')
	>>> db.session.add(u)
	>>> db.session.commit()  

Los cambios en la BD se realizan en el contexto de una sesión, a la que se puede acceder como
**db.session**. Se puede acumular varios cambios en una sesión y una vez que se hayan registrado
todos los cambios se puede emitir un único commit **db.session.commit()**. Si en algún momento
mientras trabaja en una sesión hay un error, una llamada a **db.session.rollback()** abortará la
sesión y eliminará cualquier cambio almacenado en ella. 

> Añadir otro usuario:

	>>> u = User(username='susan', email='susan@example.com')
	>>> db.session.add(u)
	>>> db.session.commit()

> La BD puede responder una consulta que retorne todos los usuarios:

	>>> users = User.query.all()
	>>> users
	[<User john>, <User susan>]

Todos los modelos tienen un atributo **query** que es el punto de entrada para hacer consultas.

> Si conozco el _id_ de un usuario puedo consultarlo:

	>>> u = User.query.get(1)

> Creamos un post:

	>>> u = User.query.get(1)
	>>> p = Post(body='my first post!', author=u)
	>>> db.session.add(p)
	>>> db.session.commit()

Con **db.session.delete** se pueden eliminar registros de la base de datos:

	>>> users = User.query.all()
	>>> for u in users:
	...     db.session.delete(u)
	...
	>>> posts = Post.query.all()
	>>> for p in posts:
	...     db.session.delete(p)
	...
	>>> db.session.commit()

### Shell Context

**flask shell** parecido al Django Shell, permite configurar las herramientas que deseo tener para
realizar pruebas y no tener que hacer los imports cada vez que trabaje con el interprete de Python.

En el modulo _microblog.py_:

	from app import app, db
	from app.models import User, Post

	@app.shell_context_processor
	def make_shell_context():
	    return {'db': db, 'User': User, 'Post': Post}

	(venv) $ flask shell
	>>> db
	<SQLAlchemy engine=sqlite:////Users/migu7781/Documents/dev/flask/microblog2/app.db>
	>>> User
	<class 'app.models.User'>
	>>> Post
	<class 'app.models.Post'>


# Parte 5 (User Logins)

### Password Hashing

**Werkzeug** es un paquete que se preinstala con Flask, ya que hace parte del nucle de este.
**Werkzeug** es importante ya que este tiene una funcionlidad que nos permite cifrar las
contraseñas.

Ejemplo:

	>>> from werkzeug.security import generate_password_hash
	>>> hash = generate_password_hash('foobar')
	>>> hash
	'pbkdf2:sha256:50000$vT9fkZM8$04dfa35c6476acf7e788a1b5b3c35e217c78dc04539d295f011f01f18cd2175f'

En el ejemplo, la contraseña 'foobar' se transformó en un string codificado a través de una serie
de operaciones criptográficas que NO tienen una operiación inversa conocida, lo que significa que 
una persona que obtiene la contraseña hash no podrá usarla para obtener la contraseña original.

Como medida adicional, si se ha cifrado la misma contraseña varias veces, se obtendrán diferentes
resultados, por lo que es imposible identificar si dos usuarios tiene la misma contraseña solo con
observar sus valores hash.

El proceso de verificación se realiza con otra función:

	>>> from werkzeug.security import check_password_hash
	>>> check_password_hash(hash, 'foobar')
	True
	>>> check_password_hash(hash, 'barfoo')
	False

Todo el proceso de cifrado de contraseñas se puede implemetar con solo dos funciones. Ver
_models.py_ clase _User_.

Practica:

	>>> u = User(username='susan', email='susan@example.com')
	>>> u.set_password('mypassword')
	>>> u.check_password('anotherpassword')
	False
	>>> u.check_password('mypassword')
	True

### Introduction to Flask-Login

La extensión **Flask-Login** controla el estado de inicio de sesión del usurio, de modo que, por
ejemplo los usuarios puede iniciar sesión en la aplicación y luego navegar a diferentes páginas
mientras la aplicación 'recuerda' que el usuario ha iniciado sesión. También proporciona la 
funcionalidad 'recordarme' que permite a los usuarios permanecer conectados incluso después de cerrar
la ventana del navegador.

	(venv) $ pip install flask-login

Como otras extensiones Flask-Login necesita ser creado he inicializado despues de la instancia de
la aplicación, en '\___init__.py'. 

### Preparing The User Model for Flask-Login

La extensión Flask-Login trabaja con el model definido en la aplicación **User** y espera que este
implemente ciertas propiedades y métodos. Este enfoque es agradable,ya que mientras estos elementos
necesarios se agreguen al modelo, Flask-Login no tiene ningún otro requisito, por lo que puede 
funcionar con modelos de usuarios basados en cualquier sistema de bases de datos.

Los items requeridos son:

1. **is_authenticated**, una propiedad que es _True_ si el usuarios tiene credenciales validas, en 
caso contrario _Flase_.

2. **is_active**, una propiedad que es _True_ si la cuenta del usuario esta activa, _False_ en 
caso contrario.

3. **is_anonymous**, una propiedad que es False para usuarios normales y True para un usuario
anónimo especial.

4. **get_id ()**, un método que devuelve un identificador único para el usuario como una cadena
(unicode, si usa Python 2).

Ya que estas implementaciones son genericas Flask-Login provee una clase _mixin_ que implementa los
4 items de forma rapida y que es compatible con la mayoria de modelos _User_. La clase **UserMixin**.

	from flask_login import UserMixin
	
	class User(UserMixin, db.Model):
	    ...

### User Loader Function

Flask-Login realiza un seguimiento del usuario que ha iniciado sesión almacenando su identificador
único en la sesión de usuario de Flask, un espacio de almacenamiento asignado a cada usurio que se
conecta a la aplicación. Cada vez que el usuario conectado navega a una página nueva, Flask-Login
recupera el ID del usuario de la sesión y luego lo carga en la memoria.

Como Flask-Login no sabe nada acerca de las bases de datos, necesita la ayuda de la aplicación para
cargar un usuario, la extensión espera que la aplicación configure una función de carga de usuarios,
que se puede llamar para cargar un usuario dado el ID.

> En app/models.py

	from app import login
	# ...

	@login.user_loader
	def load_user(id):
    	return User.query.get(int(id))

La función que carga el usuario está registrado con Flask-Login con el decorador **@login.user_loader**.
El _id_ que la extensión pasa a la función como argumento va a ser un string, por lo que las BD que usan
datos numéricos necesitan convertir la cadena en un integer.

### Logging Users In

Ver la función _login_ en _routes.py_.

La variable **current_user** proviene de Flask-Login y puede usarse en cualquier momento durante el
manejo para obtener el objeto de usuario que representa al cliente en el request.

### Logging Users Out

Para cerrar la sesión de los usuarios se puede usar la función de Flask-Login **logout_user()**.
Ver: 'app/routes.py'.

Para exponer los links de login y logout a los usuarios ver: _app/templates/base.html_.

La propiedad **is_anonymous** es un atributo que Flask-Login agrega a los objetos User a través de
la clase _UserMixin_. La expresión **current_user.is_anonymous** va a ser **True** solo cuando el
usuario no haya iniciado sesión.

### Requiring Users To Login (Exigir a los usuarios que inicien sesión)

Flask-Login proporciona una función que redirecciona a la página de inicio de sesión a los usuarios
que no esten logueados y que intenten ver una página protejida.

Para que este función sea implementada Flask-Login necesita saber cual es la vista que controla los
logins, esto se puede implementar en el archivo **app/__init__.py**.

	#
	login = LoginManager(app)
	login.login_view = 'login'

El valor _'login'_ es el nombre de la función de vista (o endpoint) que se usa en __url_for()__ para
obtener las URL.

La forma en que Flask-Login protege las vistas es con el decorador **@login_required**. Este debe estar
ubicado debajo del decorador de Flask **app.route()**, y con esto la vista quedará protegida contra
usuarios que no estén autenticados.

Ejemplo:

	from flask_login import login_required

	@app.route('/')
	@app.route('/index')
	@login_required
	def index():
		# ...

ejemplo de la implementación de **next**:

	from flask import request
	from werkzeug.urls import url_parse

	@app.route('/login', methods=['GET', 'POST'])
	def login():
	    # ...
	    if form.validate_on_submit():
	        user = User.query.filter_by(username=form.username.data).first()
	        if user is None or not user.check_password(form.password.data):
	            flash('Invalid username or password')
	            return redirect(url_for('login'))
	        login_user(user, remember=form.remember_me.data)
	        next_page = request.args.get('next')
	        if not next_page or url_parse(next_page).netloc != '':
	            next_page = url_for('index')
	        return redirect(next_page)
	    # ...

### Showing The Logged In User in Templates (Mostrando el usuario registrado en los templates)

Para ver la información de los usuarios logueados en los templates usar **current_user** de 
Flask-Login. Ver _app/templates/index.html_

> CREAR USUARIOS DESDE LA CONSOLA
	
	>>> u = User(username='susan', email='susan@example.com')
	>>> u.set_password('cat')
	>>> db.session.add(u)
	>>> db.session.commit()

### User Registration

_app/forms.py_ Clase: **RegistrationForm**.

Cuando se añade nvalidadores a los formularios y estos se nombran de la forma **validate_<field-name>**
WTFForms toma estos validadores y los añade a los que trae por defecto.

Para ver el formulario de registro: app/templates/register.html, app.routes.register, app.forms.RegisterForm
