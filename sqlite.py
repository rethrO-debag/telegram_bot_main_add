import sqlite3

class Database:
	def __init__(self, path_to_db="sport.db"):
		self.path_to_db = path_to_db

	@property
	def connection(self):
		return sqlite3.connect(self.path_to_db)

	def execute(self, sql: str, parameters: tuple = None, fetchone = False, fetchall=False, commit=False):
		
		if not parameters:
			parameters = tuple()

		connection = self.connection
		connection.set_trace_callback(logger)
		cursor = connection.cursor()

		data = None

		cursor.execute(sql, parameters)

		if commit:
			connection.commit()

		if fetchone:
			data = cursor.fetchone()

		if fetchall:
			data = cursor.fetchall()

		connection.close()

		return data

	def create_table_users(self):
		sql = """
    	CREATE TABLE users (
    		id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    		user_id   INTEGER  UNIQUE
		                       NOT NULL,
    		join_date DATETIME DEFAULT ( (DATETIME('now') ) ),
    		visible   BOOLEAN  NOT NULL
        		               DEFAULT ( (true) ) 
		);
		"""
		self.execute(sql, commit=True)

	def create_table_exercises(self):
		sql = """
    	CREATE TABLE exercises (
		    id   INTEGER PRIMARY KEY AUTOINCREMENT,
		    name         NOT NULL
		);
		"""
		self.execute(sql, commit=True)

	def create_table_results(self):
		sql = """
    	CREATE TABLE results (
		    id                    INTEGER       PRIMARY KEY,
		    exercises_id          VARCHAR       REFERENCES exercises (id) ON DELETE RESTRICT
		                                        NOT NULL,
		    approaches            INTEGER       NOT NULL,
		    number_of_repetitions INTEGER,
		    date_of_completion    DATETIME      DEFAULT ( (DATETIME('now') ) ) 
		                                        NOT NULL,
		    user_id               VARCHAR (100) REFERENCES users (user_id) 
		                                        NOT NULL
		);
		"""
		self.execute(sql, commit=True)

	def auth_user(self, user_id: int):
		sql = "INSERT INTO `users` (`user_id`) VALUES (?)"
		parameters = (user_id)
		self.execute(self, parameters=parameters, commit=True)

	#def format_args(sql, parameters: dict):
	#	sql += " AND ".join([
    #		f"{item} = ?" for item in parameters
    #		])
	#	return sql, tuple(parameters.values())

	#def select_user(self, **kwargs):
	#	sql = "SELECT * FROM users WHERE "
	#	sql = self.format_args(sql, kwargs)
	#	return self.execute(sql, parameters, fetchone=True)

	def select_exercises(self):
		sql = "SELECT name FROM exercises"
		return self.execute(sql, fetchall=true)

	def user_exists(self, user_id: int):
		sql = "SELECT `id` FROM `users` WHERE `user_id`"
		parameters = (user_id)
		return bool(self.execute(sql, fetchone=True))

def logger(statement):
	print(f"""
--------------------------------------------------------------------------------------
Executing:
{statement}
--------------------------------------------------------------------------------------
""")