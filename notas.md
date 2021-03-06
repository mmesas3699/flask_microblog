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


# Parte 6 (Profile Page and Avatars)

### User Profile Page

Para crear una página de perfil creamos una vista que mapee con la URL _/user/<username>_. (user)

Ver el template: _app/templates/user.html_

> Para resaltar que en el template _base.html_, en la creación del link para los perfiles de los
usuarios en la función **url_for()**, se para como paramentro _username_ que tiene el mismo nombre
que se usa en la definición de la vista 'user'. 

	<a href="{{ url_for('user', username=current_user.username) }}">Profile</a>

### Avatars
---

### Using Jinja2 Sub-Templates ( {% include '' %} )

Los **sub-templates** se usan con _include_ de Jinja2. 

> Una conveción que puede ser util es nombrar a estos sub-templates con _\__template.html_\

Ver: \__post.html y user.html

### More Interesting Profiles

Un problema con la página actual es que el perfil no muestra mucha información acerca de los usuarios.

Para añadir información adicional (acerca de y ultima visita), es necesario extender el model User.
Ver: app.models.User

**Recuerde que cada vez que la base de datos es modificada es necesario realizar una migración**

Ver: app/templates/user, para ver la información añadida.

### Recording The Last Visit Time For a Use

Que se ejecuten ciertos procesos antes de enviar un request a una vista solicitada es una tarea
común en las aplicaciones web y Flask lo provee por defecto:

	from datetime import datetime

	@app.before_request
	def before_request():
	    if current_user.is_authenticated:
	        current_user.last_seen = datetime.utcnow()
	        db.session.commit()

El decorador **@before_request** registra la función decorada (before_request()), para que
sea ejecutada antes de las vistas.

Lo anterior es útil porque ahora puede ejecutar el código que desee antes de que se ejecuten las
vistas.

> Se da un concejo y es que las aplicaciones web deben trabajar con unidades de tiempo consistentes
y por eso de debe usar UTC, en lugar de la hora local ya que lo que se guarde en la base de datos 
dependerá de la ubicación del usuario.

El porque no hya un **db.session.add()** antes del commit(), es poque cuando se hace referncia a
current_user, Flask-Login invoca la función (callback) para cargar el usuario (user loader callback)
que ejecuta una consulta a la BD y que colocará al usuario de destino en la sesión de la base de
datos. Asi que si lo desea puede usar db.session.add() pero no es necesario.

### Profile Editor

Se va a dar a los usuarios un formulario en el que puedan ingresar información sobre ellos mismos y
tambien les permitira cambiar su nombre de usuario.

Para lo anterios se va a crear un formulario que almacenará la informacion sobre ellos en el campo
*about_me* que se creó en el modelo User.

Ver: app/forms.py

	from wtforms import StringField, TextAreaField, SubmitField
	from wtforms.validators import DataRequired, Length

	# ...

	class EditProfileForm(FlaskForm):
	    username = StringField('Username', validators=[DataRequired()])
	    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	    submit = SubmitField('Submit')

El template que almacenará este formulario es: app/templates/edit_profile.html

La vista para manejar este formulario es: app.routes.edit_profile


# Parte 7 Error Handling (Manejo de Errores)

¿Que ocurre cuando hay un erro en una aplicación de Flask?.

### Debug Mode

Para mantener el servidor protejido el modo DEBUG de Flask se debe ejecutar solo en un ambiente
de desarrollo.

Para activar el modo 'debug':

	(venv)$ export FLASK_DEBUG=1

### Custom Error Pages

Flask provee una forma de crear nuestars propias páginas de errores.

En este caso se van a definir páginas de errores para los HTTP 404 y 500.

Para crear un controlador de errores propio se usa el decorador: **@errohandler**. En este caso
se van a poner los controladores de errores en el modulo: **app/errors.py**

Para registrar los controladores de errores, se debe importar el modulo *errors.py*, despues de
la creación de la instancia de la aplicación.

	app/__init__.py: Import error handlers

	# ...

	from app import routes, models, errors

### Sending Errors by Email

El otro problema con el manejo de errors predeterminado de Flask es que no tiene notificaciones, el
seguimiento de la pila para los errores se imprime en la terminal, lo obliga a monitorear la salida
del proceso del servidor para descubiri errores. Cuando se ejecuta la aplicación en ambiente de
desarrollo no hay ningín problema, pero en un servidor de producción, nadie va a revisar la terminal,
por lo que se debe implementar una solución más solida.

**Es muy importante tomar un posición proactiva con respecto a los errores.**

si ocurre un error en la versión de producción de la aplicación, es necesario saberlo de inmediato.
Por lo tanto se va a configurar Flask para que envíe un correo inmediatamente deśpués de un error, 
y en el cuerpo del correo estara la pila de errores.

El primer paso es agregar los detalles del servidor de correo electrónico al archivo de
configuración:

Ver config.py:

	class Config(object):
    	# ...
	    MAIL_SERVER = os.environ.get('MAIL_SERVER')
	    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	    ADMINS = ['your-email@example.com']

La opción **ADMINS** almacena en una lista las direcciones a las cuales se les enviaran los logs.

Flask usa el paquete Python **logging** para escribir sus logs, y este paquete tiene la posibilidad
de enviar sus logs por email.

Todo lo que se necesita para recibir correos enviados sobre errores es agregar una instancia de
**SMTPHandler** al objeto logger Flask, que es app.logger:

Ver: app/__init.py__

	import logging
	from logging.handlers import SMTPHandler

	# ...

	if not app.debug:
	    if app.config['MAIL_SERVER']:
	        auth = None
	        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
	            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
	        secure = None
	        if app.config['MAIL_USE_TLS']:
	            secure = ()
	        mail_handler = SMTPHandler(
	            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
	            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
	            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
	            credentials=auth, secure=secure)
	        mail_handler.setLevel(logging.ERROR)
	        app.logger.addHandler(mail_handler)

Para probar esta configuración hay que usar una cuenta de Google.

	export MAIL_SERVER=smtp.googlemail.com
	export MAIL_PORT=587
	export MAIL_USE_TLS=1
	export MAIL_USERNAME=<your-gmail-username>
	export MAIL_PASSWORD=<your-gmail-password>

### Logging to a File

Recibir errores por mail es bueno, pero aveces no es suficiente. Hay algunas condiciones de falla
que no terminan en una excepción de Python y no son un problema importante, pero aún pueden ser lo
suficientemente interesantes como para guardarlas con fines de depuración.

Para habilitar un log basado en archivos, otro manejador, esta vez de tipo **RotatingFileHandler**,
este debe estar conectado al registro de aplicaciones, de forma similar al controlador de email.

Ver: app/__init__.py

	# ...
	from logging.handlers import RotatingFileHandler
	import os

	# ...

	if not app.debug:
	    # ...

	    if not os.path.exists('logs'):
	        os.mkdir('logs')
	    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
	                                       backupCount=10)
	    file_handler.setFormatter(logging.Formatter(
	        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	    file_handler.setLevel(logging.INFO)
	    app.logger.addHandler(file_handler)

	    app.logger.setLevel(logging.INFO)
	    app.logger.info('Microblog startup')


Se va a escribir el archivo de registro con el nombre de 'microblog.log' es un directorio de logs,
el cual se crea se no existe.

La clase **RotatingFileHandler** es muy útil porque rota los registros, lo que garantiza que los
archivos de registro no crezcan demasiado cuando la aplicación se ejecuta durante mucho tiempo. En
este caso se esta limitando el tamaño del archivo de registro a 10KB, y se guardan los últimos 10 logs
como copia de seguridad.

La clase **logging.Formatter** proporciona un formato personalizaod para los mensajes de registro. Como
estos mensje van a un archivo, se quiere que tengan tanta información como sea posible. Asi que se
usa un formato que incluye la marca de tiempo (timestamp), el nivel de registro, el mensaje, el
archivo fuente y el número de línea desde donde se originó la entrada del registro. También se baja
el nivel de registro a la categoria INFO, tanto en el registrador de aplicaciones como en el manejador
de registro de archivos.

> Importante: Las categorias de registro son: DEBUG, INFO, WARNING, ERROR, CRITICAL, en orden creciente
de severidad. Como primer uso interesante del archvio de log, el servidor escribe una línea en los
registros cada vez que se inicia. Cuando esta aplicación se ejecuta en un servidor de producción,
estas entradas de registro le indicarán cuándo se reinició el servidor.

### Fixing the Duplicate Username Bug

Ver: app.forms.EditProfileForm:

	class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

Ver: app.routes.edit_profile

	@app.route('/edit_profile', methods=['GET', 'POST'])
	@login_required
	def edit_profile():
    	form = EditProfileForm(current_user.username)
    	# ...


# Parte 8 (Followers)

### Database Relationships Revisited

En este capítulo se va a trabajar mas con la base de datos de la aplicación. Se requiere que los
usuarios de la aplicación puedan elegir facilmente a que otros usuarios quieren seguir.

Se ha dicho que se quiere crear una lista de usuarios seguidos y no seguidos, pero las bases de
datos relacionales no tienen un tipo de dato 'lista' que se pueda usar para este caso. Todo lo
que hay dentro de las bases de datos son tablas con registros y relaciones entre los registros.

La base de datos en este momento tiene una tabla que representa los Usuarios, por lo tanto solo
queda crear la relación correcta que represente la relación de follow/followed.

### One-To-Many

![One-ToMany](./adjuntos_notas/ch04-users-posts.png)

Las dos entidades en esta relación son 'usuarios' y 'posts'. Se djo que un usuario podria tener
muchos posts y un post solo un usuario. La relación es representada en la base de datos con
una llave foranea en el lado de 'many' (muchos). En esta relación la llave foramena es el campo
**user_id** de la tabla Posts, y este camop representa el vinculo entre el post y el usuario 
en la tabla User.

Está bastante claro que el campo **user_id** provee una relación directa con su autor, pero y que
hay de la dirección inversa. Para quela relación sea útil, se debería poder obtener la lista de
post escritos por un usuario. El campo user_id en la tabla de Posts es suficiente para responder
esta inquietud, ya que las bases de datos tiene índices que permiten consultas eficientes como:
"recuperar todas las publicaciones que tienen un user_id X".

### Many-To-Many

Las relaciones de muchos a muchos son un poco más complejas. 
Ejemplo: Considere una base de datos que tenga estudiantes y profesores. Se puede decir que un alumno
tiene muchos profesores y un maestro tiene muchos alumnos. Es como dos relaciones superpuestas de uno
a muchos desde ambos extremos.

Para una relación de este tipo, debería poder consultar la BD y obtener la lista de docentes que
enseñan a un alumno determinado y la lista de alumnos de una clase de docente. Para poder representar
esto en una BD relacional, se requiere el uso de una tabla auxiliar llamada tabla de asociación. Ya
que no se puede hacer agregando llaves foraneas a las tablas existentes.

![Many-To-Many](./adjuntos_notas/ch08-students-teachers.png)

### Many-to-One and One-to-One

La relación muchos-a-uno es igual a uno-a-muchos la unica diferencia es que la relación es vista
desde el lado de muchos.

Una relación uno-a-uno es un caso especial de uno-a-muchos. La representación es similar, pero se
agrega un constrain (restricción) a la BD para evitar que el lado 'muchos ' tenga más de un enlace.
Si bien hay casos en los que este tipo de relación es útil, no es tan común como lo otros tipos.

### Representing Followers (Representando seguidores)

Se va a usar la representación Many-To-Many porque un usuario puede seguir muchos usuarios y un
usuario puede tener muchos seguidores. Pero con una variación, en el ejemplo de los profesores y 
estudiantes habian dos entidades, maestros y alumnos. Pero en el caso de los seguidores hay usuarios
siguiendo usuarios, asi que solo tengo la entidad usuarios.

Una relación ne la que las instancias de una clase están vinculadas a otras de la misma clase de llama
relación autorreferencial (self-referential relationship).

Aquí hay un diagrama de la relación autorreferencial de muchos a muchos que hace un seguimiento de
los seguidores:

![self-referential relationship](./adjuntos_notas/ch08-followers-schema.png)

### Database Model Representation

Para añadir seguidores a la base de datos. Primero aquí esta la tabla asociativa **followers**.

Ver: app/models.py

	followers = db.Table('followers',
	    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
	)

Esto es una traducción directa de la tabla asociativa del diagrama anterior. Note que no se
declara la tabla como un modelo, asi como se hizo con las tablas User y Post. Ya que esto es una
tabla auxiliar y no va a contener datos más allá de las llaves foraneas, se crea sin la
herencia de la clase db.Model.

Para crear la relación Many-To-Many en la tabla User:

	class User(UserMixin, db.Model):
    # ...
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


Se usa la función **db.relationship** para definir la relación en la clase Model. Esta relación
vincula las instancias de User con otras instancias de User, por conveción, digamos que para un
par de usuarios vinculados por esta relación, el usuario del lado izquierdo está siguiendo (followed)
al usuario del lado derecho. Se define la relación como se ve desde el lado izquierdo con el nombre
_followed_, porque cuando se ahga una consulta desde el lado izquierdo se obtendra una lista de
usuarios seguidos (es decir los del lado derecho).

Revisando los argumentos de la función **db.relationship**:

- 'User' es la entidad del lado derecho de la relación (la entidad del lado izquierdo es la clase
principal). Como esta es una relación autorreferencial, tengo que usar la misma clase en ambos lados.

- _secondary_ configura la tabla de asociación que se usa para esta relación, que definí justo arriba
de esta clase.

- _primaryjoin_ indica la condición que vincula la entidad del lado izquierdo (el usuario seguidor)
con la tabla de asociación. La condición de unión (join) para el lado izquierdo es el ID de usuario que
coincide con la columna **follower_id** de la labla de asociación. La expresión *followers.c.follower_id*
hace referencia a la columna *follower_id* de la tabla de asociación.

- _secondjoin_ indica la condición que vincula la entidad del lado derecho (el usuario seguido) con
la tabla de asociación. Es similar a la de _primaryjoin_ pero con la diferencia de que ahora se usa
*followed_id*, que es la otra llave foranea en la tabla de asociación.

- _backref_ define cómo se accederá a esta relación desde la entidad del lado derecho. Desde el lado
izquierdo, la relazión se nombra *followed*, pero desde el lado derecho se va a usar *followers*
para representar a todos los usuarios del lado izquierdo que están vinculados al usuario objetivo
en el lado derecho. El argumento _lazy_ adicional indica el modo de ejecución para la consulta. El 
modo dinámico configura la consulta para que no se ejecute hasta que se solicite específicamente.

- _lazy_ es similar al parámetro del mismo nombre en _backref_, pero este se aplica a la consulta del
lado izquierdo en lugar del lado derecho.

> Recuerde: siempre que se hagan cambios en los modelos hay que hacer las migraciones.

	(venv) $ flask db migrate -m "followers"
	(venv) $ flask db upgrade

### Adding and Removing "follows"

Gracias al ORM de SQLAlchemy, un usuario que sigue a otro puede ser registrado en la BD utilizando
la relación _followed_ como si fuera una lista. Por ejemplo:

	user1.followed.append(user2)

Y para dejar de seguirlo:

	user1.followed.remove(user2)

A pesar de que agregar y elimnar seguidores es bastante fácil, se quiere (siempre) promover la
reutilización del código, por eso no se va a esparcir 'agregar' y 'eliminar' a través del código.
en su lugar se van a crear la funciones: "follow" "unfollow" como métodos del model User.

> Siempre es mejor alejar la lógica de la aplicación de las funciones de vista y pasarla a los modelos
u otras clases o módulos auxiliares, ya que esto hace que realizar 'unit testing' sea más sencillo.

Cambios en el modelo User:

	class User(UserMixin, db.Model):
	    #...

	    def follow(self, user):
	        if not self.is_following(user):
	            self.followed.append(user)

	    def unfollow(self, user):
	        if self.is_following(user):
	            self.followed.remove(user)

	    def is_following(self, user):
	        return self.followed.filter(
	            followers.c.followed_id == user.id).count() > 0

### Obtaining the Posts from Followed Users

En la página de indice de la aplicación, voy a mostrar las publicaciones de blog escritas por
todas las personas seguidas por el usuario que inició sesión.

Para obtener los posts es necesario hacer una consulta a la base de datos, pero cual es la mejor
forma de hacerlo.

Se puede hacer un query que traiga un listado de todos los usuarios seguidos y con esta lista
hacer otro que traiga y una los posts por cada usuario en la lista, admeas de tener que ordenarlos.
Esto es ineficiente, ya que si el usuario sigue a otros mil, voy a manejar toda esta información en
memoria y es un uso bastante ineficiente.

Realmente no hay manera de evitar esta fusión y clasificación de las publicaciones del blog,
pero hacerlo en la aplicación resulta en un proceso muy ineficiente. **Este tipo de trabajo es en
el que sobresalen las bases de datos relacionales**.

Las BD que tiene inidces que les permiten realizar las consultas y la clasificación de una manera
mucho más eficiente que hacerlo desde la aplicación.

	class User(db.Model):
	    #...
	    def followed_posts(self):
	        return Post.query.join(
	            followers, (followers.c.followed_id == Post.user_id)).filter(
	                followers.c.follower_id == self.id).order_by(
	                    Post.timestamp.desc())

Dentro de la consulta hay tres secciones principales: join(), filter(), order_by(), que son métodos
del objeto _query_ de SQLAlchemy.

### Unit Testing the User Model

Cada vez que se crean caracteristicas algo complejas, es recomendable realizar pruebas unitarias.

Python incluye el paquete **unittest** el cual facilita la escritura y ejecución de pruebas unitarias.
Estas pruebas irán en el modulo _tests.py_.

Para ejecutar las pruebas:

	(venv)$ python tests.py

Los métodos **setUp()** y **tearDown()** son métodos especiasles que se ejecutan antes y despues de
cada prueba respectivamente. Se implmenteo un hack en setUp(), para evitar que las pruebas utilicen
la BD reular usada en desarrollo. La cambiar la configuración a sqllite:// se obtiene que SQLAlchemy
use una base de datos SQLite en memoria durante las pruebas. La llamada a *db.create_all()* crea
todas las tablas de la base de datos. Es una forma útil y rápida para crear una base de datos desde
cero muy útil para pruebas más no para desarrollo o producción, en estos casos usar las migraciones.

### Integrating Followers with the Application

Se añaden dos neuvas rutas para 'follow' y 'unollow':

	@app.route('/follow/<username>')
	@login_required
	def follow(username):
	    user = User.query.filter_by(username=username).first()
	    if user is None:
	        flash('User {} not found.'.format(username))
	        return redirect(url_for('index'))
	    if user == current_user:
	        flash('You cannot follow yourself!')
	        return redirect(url_for('user', username=username))
	    current_user.follow(user)
	    db.session.commit()
	    flash('You are following {}!'.format(username))
	    return redirect(url_for('user', username=username))

	@app.route('/unfollow/<username>')
	@login_required
	def unfollow(username):
	    user = User.query.filter_by(username=username).first()
	    if user is None:
	        flash('User {} not found.'.format(username))
	        return redirect(url_for('index'))
	    if user == current_user:
	        flash('You cannot unfollow yourself!')
	        return redirect(url_for('user', username=username))
	    current_user.unfollow(user)
	    db.session.commit()
	    flash('You are not following {}.'.format(username))
	    return redirect(url_for('user', username=username))

Modificando: app/templates/user.html


# Parte 9 (Pagination)

### Submission of Blog Posts

El home page necesita tener un formulario para que los usuarios puedan escribir nuevos posts.

Ver: app/forms.py

	class PostForm(FlaskForm):
	    post = TextAreaField('Say something', validators=[
	        DataRequired(), Length(min=1, max=140)])
	    submit = SubmitField('Submit')

Despues añadir este formulario a index.html.

	{% extends "base.html" %}

	{% block content %}
	    <h1>Hi, {{ current_user.username }}!</h1>
	    <form action="" method="post">
	        {{ form.hidden_tag() }}
	        <p>
	            {{ form.post.label }}<br>
	            {{ form.post(cols=32, rows=4) }}<br>
	            {% for error in form.post.errors %}
	            <span style="color: red;">[{{ error }}]</span>
	            {% endfor %}
	        </p>
	        <p>{{ form.submit() }}</p>
	    </form>
	    {% for post in posts %}
	    <p>
	    {{ post.author.username }} says: <b>{{ post.body }}</b>
	    </p>
	    {% endfor %}
	{% endblock %}

Y por ultimo crear una vista para la creación de posts.
Ver: app/routes.py

	from app.forms import PostForm
	from app.models import Post

	@app.route('/', methods=['GET', 'POST'])
	@app.route('/index', methods=['GET', 'POST'])
	@login_required
	def index():
	    form = PostForm()
	    if form.validate_on_submit():
	        post = Post(body=form.post.data, author=current_user)
	        db.session.add(post)
	        db.session.commit()
	        flash('Your post is now live!')
	        return redirect(url_for('index'))
	    posts = [
	        {
	            'author': {'username': 'John'},
	            'body': 'Beautiful day in Portland!'
	        },
	        {
	            'author': {'username': 'Susan'},
	            'body': 'The Avengers movie was so cool!'
	        }
	    ]
	    return render_template("index.html", title='Home Page', form=form,
	                           posts=posts)

> Es un estándar usar **redirect** después de un POST ya que con esto se evita el tener información
duplicada. Si la ultima vez se envió un formulario por POST y se recarga la página, el navegador
va a reenviar el formulario y podría duplicarse la información. Esto es un patrón llamado 'Post/Redirect/Get'.

### Displaying Blog Posts

Ver: app/routes.py

	@app.route('/', methods=['GET', 'POST'])
	@app.route('/index', methods=['GET', 'POST'])
	@login_required
	def index():
	    # ...
	    posts = current_user.followed_posts().all()
	    return render_template("index.html", title='Home Page', form=form,
	                           posts=posts)

### Making It Easier to Find Users to Follow

Se va a crear una página "Explorar". Esta página funcionará como la página de inicio, pero en lugar
de mostrar solo las publicaciones de los usuarios seguidos, mostrará una secuiencia de publicaciones
globales de todos los usuarios.

Ver: app.routes.explore

Nótese que en la función *render_template()* se llama a 'index.html', esto porque se decidió utilizar
esta plantilla, ya que esta página va a ser muy similar a la página principal. La única diferencia
es que esta no va a tener el formulario para escribir nuevos posts.

Para evitar que el template genere errores se colocó una condición para que se muestre el formulario
solo si este se paga como parametro.

Ver: app/templates/index.html

	{% extends "base.html" %}

	{% block content %}
	    <h1>Hi, {{ current_user.username }}!</h1>
	    {% if form %}
	    <form action="" method="post">
	        ...
	    </form>
	    {% endif %}
	    ...
	{% endblock %}

### Pagination of Blog Posts

Flask-SQLAlchemy permite la paginación de forma nativa en el método **paginate()**. Si por ejemplo,
deseo obtener las primeras 20 publicaciones seguidas del usuario, se puede reemplazar _all()_ :

	>>> user.followed_posts().paginate(1, 20, False).items

El método paginate() se puede llamar desde cualquier objeto query de SQLAlchemy, y toma 3 argumentos:

- El número de la página, empezando con 1.
- El número de items por página.
- Una bandera de error. Si es True, cuando se solicite una página fuera de rango, se devolverá
automáticamente un error 404. Si es False, se devolverá una lista vacia para las páginas fuera de
rango.

El valor devuelto por paginate() es un objeto **Pagination**. El atributo **items** de este objeto
contiene la lista de elementos en la página solicitada.

Para implementar la paginación lo primero es configurar la variable **POST_PER_PAGE**, que determina
cuantos objetos se mostraran por página.

	class Config(object):
	    # ...
		POSTS_PER_PAGE = 3

Después de esto es necesario decidir como se van a incorporar los números de la páginas en las URLs
de la aplicación. La forma más común es colocar un query string como argumento especificando un número
opcional de página, dejando por defecto 1 si este argumento no es pasado.

Ejemplos de como se va a implementar:

1. Page 1: implicit: http://localhost:5000/index
2. Page 2: explicit: http://localhost:5000/index?page=1
3. Page 3: http://localhost:5000/index?page=3

Para acceder a los argumentos de las URL Flask usa el objeto **request.args**.

Ver app/routes.py

	@app.route('/', methods=['GET', 'POST'])
	@app.route('/index', methods=['GET', 'POST'])
	@login_required
	def index():
	    # ...
	    page = request.args.get('page', 1, type=int)
	    posts = current_user.followed_posts().paginate(
	        page, app.config['POSTS_PER_PAGE'], False)
	    return render_template('index.html', title='Home', form=form,
	                           posts=posts.items)

	@app.route('/explore')
	@login_required
	def explore():
	    page = request.args.get('page', 1, type=int)
	    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
	        page, app.config['POSTS_PER_PAGE'], False)
	    return render_template("index.html", title='Explore', posts=posts.items)

Con estos cambios, las dos vistas determinan el número de la página, puede ser del argumento **page**
o por defecto 1, después se usa el método **paginate()** para resivir solo los resultados deseados
para la página.

> Tenga en cuenta lo fáciles que son estos cambios y lo poco que se ve afectado el código cada vez
que se realiza un cambio. Estoy tratando de escribir cada parte de la aplicación sin hacer suposiciones
sobre cómo funcionan las otras partes, y esto me permite escribir aplicaciones modulares y robustas que
son más fáciles de ampliar y probar, y tienen menos probabilidades de fallar o tener errores.

Ver: http://localhost:5000/explore?page=2

### Page Navigation

El siguiente cambio es añadir links al final del listado de posts que permitan la navegación
a los usuarios.

Anteriormente se mencionó que la función **paginate()** retornaba un objeto de la clase **Pagination**
de Flask_SQLAlchemy, hasta el momento se ha usado el atributo 'items' que contiene el listado de
items recibidos para la página solicitada. Pero el objeto **Pagination** tiene otros atributos
que serán utiles para la navegación:

- **has_next**: True si queda al menos una página despues de la actual.
- **has_prev**: True si hay al menos una página antes de la actual.
- **next_num**: El número de la siguiente página.
- **prev_num**: El número de la página previa.

Con estos cuatro elementos se va a generar la navegación de los posts:

Ver: app/routes.py

	@app.route('/', methods=['GET', 'POST'])
	@app.route('/index', methods=['GET', 'POST'])
	@login_required
	def index():
	    # ...
	    page = request.args.get('page', 1, type=int)
	    posts = current_user.followed_posts().paginate(
	        page, app.config['POSTS_PER_PAGE'], False)
	    next_url = url_for('index', page=posts.next_num) \
	        if posts.has_next else None
	    prev_url = url_for('index', page=posts.prev_num) \
	        if posts.has_prev else None
	    return render_template('index.html', title='Home', form=form,
	                           posts=posts.items, next_url=next_url,
	                           prev_url=prev_url)

	@app.route('/explore')
	@login_required
	def explore():
	    page = request.args.get('page', 1, type=int)
	    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
	        page, app.config['POSTS_PER_PAGE'], False)
	    next_url = url_for('explore', page=posts.next_num) \
	        if posts.has_next else None
	    prev_url = url_for('explore', page=posts.prev_num) \
	        if posts.has_prev else None
	    return render_template("index.html", title='Explore', posts=posts.items,
	                          next_url=next_url, prev_url=prev_url)

> Un aspecto interesante de **url_for()** es que se pueden añadir argumentos como diccionarios
(keywords), y si los nombres de estos argumentos no están referenciados directamente en las URL,
entonces Flask los incluirá directamente como query arguments.

La paginación se implementará en el template: index.html


