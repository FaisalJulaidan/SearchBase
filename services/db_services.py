import os
import sqlite3
from contextlib import closing

import sqlalchemy.exc

from models import Callback,\
    Company, db

APP_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = APP_ROOT + "/database.db"


class db_services:
    # def addCompanyAndUserAndRole(self):
    #     db.session.add(Role(Name="Admin", EditChatbots=True, EditUsers=True, AccessBilling=False))
    #     db.session.add(Role(Name="User", EditChatbots=True, EditUsers=True, AccessBilling=False))
    #     _safeCommit()
    #
    #     self.addCompany()
    #     self.addUser()
    #
    #
    #     # return _safeCommit()

    def addCompany():
        companyObject = Company(Name="xyz", Size="1-10", URL="www.test.com")
        db.session.add(companyObject)
        return _safeCommit()



    # ====\ Database CRUD Operations /====
    def update(sql_statement, array_of_terms):
        msg = "Error"
        conn = None
        try:
            conn = sqlite3.connect(database)
            cur = conn.cursor()
            cur.execute(sql_statement, array_of_terms)
            conn.commit()
            msg = "Record successfully updated."
        except sqlite3.ProgrammingError as e:
            msg = "Error in update statement" + str(e)
        except sqlite3.OperationalError as e:
            msg = "Error in update operation" + str(e)
        finally:
            if conn is not None:
                conn.rollback()
                conn.close()
            print(msg)
            return msg

    def get(query, args=(), one=False):
        cur = g.db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        if "SELECT" in query:
            for record in rv:
                for key, value in record.items():
                    if type(value) == bytes and "Password" not in key:
                        record[key] = encryption.decrypt(value).decode()
        return (rv[0] if rv else None) if one else rv

    # facilitate querying data from the database.

    def insert(table, fields=(), values=()):
        # g.db is the database connection
        cur = g.db.cursor()
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table,
            ', '.join(fields),
            ', '.join(['?'] * len(values))
        )
        cur.execute(query, values)
        g.db.commit()
        row = query_db("SELECT * FROM " + table + " WHERE ID=?", [cur.lastrowid], one=True)
        cur.close()
        return row

    # def delete(table, primary_key):

    def count_db(table, condition="", args=()):
        cur = g.db.execute("SELECT count(*) FROM " + table + " " + condition, args)
        return cur.fetchall()[0][0]

    # encryption function to save typing
    def encryptVar(var):
        return encryption.encrypt(var.encode())

    # ====\ Database (Connection & Initialisation) /====

    # Connects to the specific database.
    def connect_db():
        return sqlite3.connect(DATABASE)

    # Initializes the database with test data while in debug mode.
    def init_db():
        with closing(connect_db()) as db:
            with app.open_resource(APP_ROOT + '/sql/schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
            print("Database Initialized...")

            if app.debug:
                with app.open_resource(APP_ROOT + '/sql/devseed.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                    # Create and store a hashed password for "test" user
                    hash = hashPass("test")
                    update("UPDATE Users SET Password=? WHERE ID=?", [hash, 1])
                db.commit()
                print("Test Data Inserted...")

        print("Database Initialized")

    # Get connection when no requests e.g Pyton REPL.
    def get_connection():
        db = getattr(g, '_db', None)
        if db is None:
            db = g._db = connect_db()
        return db


def _safeCommit(data):
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        db.session.rollback()
        return (Callback(False, exc.orig))

    if data:
        return (Callback(True, None, data))
    else:
        return (Callback(True, None))
