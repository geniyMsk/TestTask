import sqlite3
class DBCommands:


    CREATE_CARDS = """CREATE TABLE IF NOT EXISTS cards(id INTEGER UNIQUE, photo VARCHAR(250), caption TEXT, price INTEGER)"""
    CREATE_USERS = """CREATE TABLE IF NOT EXISTS users (fullname TEXT, username TEXT, chatid INTEGER UNIQUE, zakaz JSON)"""
    async def create(self):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            cursor.execute(self.CREATE_USERS)
            cursor.execute(self.CREATE_CARDS)

    SELECT_ID = """SELECT id FROM cards"""
    async def select_id(self):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_ID
            return cursor.execute(command)

    SELECT_PHOTO = """SELECT photo FROM cards WHERE id =$1"""
    async def select_photo(self, id):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_PHOTO
            return cursor.execute(command, id)

    SELECT_CAPTION = """SELECT caption FROM cards WHERE id =$1"""
    async def select_caption(self, id):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_CAPTION
            return cursor.execute(command, id)

    SELECT_PRICE = """SELECT price FROM cards WHERE id =$1"""
    async def select_price(self, id):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_PRICE
            return cursor.execute(command, id)

    UPDATE_PRICE = """UPDATE cards SET price = $1 WHERE id = $2"""
    async def update_price(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.UPDATE_PRICE
            cursor.execute(command, par)

    ADD_CARD = """INSERT INTO cards (id, photo, caption) VALUES ($1, $2, $3)"""
    async def add_card(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.ADD_CARD
            cursor.execute(command, par)

    DELETE_CARD = """DELETE FROM cards WHERE id = $1"""
    async def delete_card(self, id):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.DELETE_CARD
            return cursor.execute(command, id)

    SELECT_FULLNAME = """SELECT fullname FROM users WHERE chatid = $1"""
    async def select_fullname(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_FULLNAME
            return cursor.execute(command, chatid)

    SELECT_USERNAME = """SELECT username FROM users WHERE chatid = $1"""
    async def select_username(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_USERNAME
            return cursor.execute(command, chatid)

    SELECT_CHATID = """SELECT chatid FROM users"""
    async def select_chatid(self):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_CHATID
            return cursor.execute(command)

    SELECT_ZAKAZ = """SELECT zakaz FROM users WHERE chatid = $1"""
    async def select_zakaz(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_ZAKAZ
            return cursor.execute(command, chatid)

    UPDATE_ZAKAZ = """UPDATE users SET zakaz = $1 WHERE chatid = $2"""
    async def update_zakaz(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.UPDATE_ZAKAZ
            cursor.execute(command, par)

    SELECT_USER = """SELECT count(*) FROM users WHERE chatid = $1"""
    async def select_user(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_USER
            return cursor.execute(command, chatid)

    ADD_USER = """INSERT INTO users (fullname, username, chatid, zakaz) VALUES ($1, $2, $3, $4)"""
    async def add_user(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.ADD_USER
            cursor.execute(command, par)










