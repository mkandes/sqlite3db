#!/usr/bin/env python
#
# TODO: Add support for in-memory databases.

import contextlib
import logging
import os
import sqlite3
import sys

#logging.basicConfig(level=logging.DEBUG)

class SQLite3DB(object):
    """A simple wrapper class for working with sqlite3 databases.

    This wrapper class is intended to help simplify your programmatic
    interactions with sqlite3 databases in Python. It'll allow you to 
    quickly create a database object and begin executing SQL 
    statement(s) against it. There is no need to worry about opening
    connections to the database, creating database cursors on those 
    connections, or tracking what connections and/or cursors are opened
    or closed at any given time. All of this boilerplate housekeeping
    code is handled by the class' methods for you. The aim here is to 
    simply get you working with your database sooner rather than later.

    Check out the example database interactions in the class' main 
    function below.

    Attributes:
      database: str: required: Path to sqlite3 database.

    Methods:
      connect(): Open and return a connection to the database.
      dump(): Dump the database to an ASCII text file.
      execute(sql): Execute SQL statement(s).
      test(): Run a test SQL query against the database.
      #cache(): Load database into memory with shared cache.
      #replicate(): Replicate in-memory database across mutliple processes.
 
    """

    def __init__(self, database=None):
        """ Initializes SQLite3DB object.

        Arguments:
          database: str: required: Path to sqlite3 database.

        Returns:
          None

        Raises:
          TypeError: database argument is NOT A STRING.
          ValueError: database argument string is EMPTY.

        """

        # Start initialization of SQLite3DB object.
        logging.info(('Initializing SQLite3DB object: '
                      '{}').format(self.__repr__()))

        # Check if database argument is a string. If it is not a string, 
        # then throw an exception.
        logging.info('Type checking database argument ...')
        try:
            if not isinstance(database, str):
                raise TypeError(('database argument is NOT A STRING: '
                                 '{}').format(type(database)))
        except TypeError as e:
            logging.exception(e)
            logging.debug('database argument MUST BE A STRING.')
            raise
        else:
            logging.info(('database argument is of type: '
                          '{}').format(type(database)))

        # Check if database argument string is empty. If the string is 
        # empty, then throw an exception.
        logging.info('Checking if database argument string is empty ...')
        try:
            if not database:
                raise ValueError('database argument string is EMPTY.')
        except ValueError as e:
            logging.exception(e)
            logging.debug('database argument string CANNOT BE EMPTY.')
            raise
        else:
            logging.info(('database argument string is not empty: '
                          '{}').format(database))

        # Check if database argument string is a path to an existing 
        # file. If the file does not exist, then throw a warning. In 
        # either case, assign class instance variable self.database the 
        # absolute path of the file indicated by the database argument 
        # string.
        logging.info('Checking if database argument string is a path '
                     'to an existing file ...')
        try:
            if not os.path.isfile(database):
                raise FileNotFoundError(('database argument string is '
                                         'NOT A PATH TO AN EXISTING '
                                         'FILE: {}'.format(database)))
        except FileNotFoundError as w:
            logging.warn(w)
            logging.debug('If database file does not exist prior to '
                          'instantiation of the SQLite3DB object, an '
                          'empty sqlite3 database file will be created '
                          'at the path specified by the database '
                          'argument string upon the first connection '
                          'established to the database.')
        else:
            logging.info('database argument string is a path to an '
                         'existing file.')
        finally:
            self.database = os.path.abspath(database)
            logging.info(('Absolute path to database file is: '
                          '{}'.format(self.database)))

        # End initialization of SQLite3DB object.
        logging.info(('SQLite3DB object initialized: '
                      '{}').format(self.__repr__()))


    def connect(self):
        """ Open and return a connection to the database. 

        Arguments:
          None

        Returns:
          connection: sqlite3.Connection: A connection to the database 
              that enforces foreign key constraints.
        
        Raises:
          sqlite3.OperationalError: Unable to open database file.
          sqlite3.ProgrammingError: Cannot operate on a closed cursor or database.

        """

        # Establish a connection to the database.
        logging.info('Attempting to establish a connection to the '
                     'database ...')
        try:
            connection = sqlite3.connect(self.database)
        except sqlite3.OperationalError as e:
            logging.exception(e)
            logging.debug('Check permissions on the database file. '
                          'database file must be readable to establish '
                          'a connection.')
            raise
        else:
            logging.info(('connection established: '
                          '{}').format(connection))

        # Create a database cursor on the connection.
        logging.info('Creating a database cursor on the connection ...')
        try:
            cursor = connection.cursor()
        except sqlite3.ProgrammingError as e:
            logging.exception(e)
            raise
        else:
            logging.info(('cursor created: {}').format(cursor))

        # Enable foreign key constraints on database connection.
        logging.info('Enabling foreign key constraints ... ')
        try:
            cursor.execute('PRAGMA foreign_keys = ON;')
        except Exception as e:
            logging.exception(e)
            raise
        else:
            cursor.execute('PRAGMA foreign_keys;')
            if cursor.fetchone()[0] == 1:
                logging.info('Foreign key constraints enabled.')

        # Close database cursor.
        logging.info('Closing database cursor ...')
        try:
            cursor.close()
        except Exception as e:
            logging.exception(e)
            raise
        else:
            logging.info(('cursor closed: {}').format(cursor))

        # Return database connection.
        logging.info(('Returning database connection: '
                      '{}').format(connection))

        return connection


    def dump(self):
        """ Dump the database to an ASCII text file.

        This method provides the same capabilities as the .dump command
        in the sqlite3 shell.
 
        Arguments:
          None

        Returns:
          None

        Raises:
          Exception: Catch-all exception used until specific exceptions
              that may occur while dumping the database out to a file 
              are known.

        """

        # Dump the database to an ASCII text file.
        logging.info('Dumping database to an ASCII text file ...')
        try:
            with contextlib.closing(self.connect()) as connection:
                with connection:
                    logging.info('Opening file ...')
                    with open(self.database + '.sql', 'w') as sql_file:
                        logging.info(('file open: {}').format(sql_file))
                        sql_dump = connection.iterdump()
                        logging.info('Dumping database ...') 
                        for sql_line in sql_dump:
                            sql_file.write(('{}\n').format(sql_line))
                        logging.info('Dump complete.')
                        logging.info('Closing file ...')
                    logging.info(('file closed: {}').format(sql_file))
                logging.info('Closing database connection ...')
            logging.info(('connection closed: {}').format(connection))
        except Exception as e:
            logging.exception(e)
            raise
        else:
            logging.info(('database dumped to ASCII text file: '
                          '{}').format(self.database + '.sql'))


    def execute(self, sql=None):
        """ Executes SQL statement(s).

        This method executes SQL statement(s) against the database using
        one of three different possible modes of operation:

          NORMAL: Executes a SQL statement from a string provided as 
                  the input sql argument.

          SCRIPT: Executes all SQL statements found in a file whose
                  relative or absolute path is provided as the input 
                  sql argument.

            MANY: Executes a SQL statement from a string found at the
                  top of a list provided as the input sql argument. It
                  is executed against all parameters or mapping found
                  in the list of tuples that follow the string.

        Arguments:
          sql: str/list: required: SQL statement(s) to be executed. 

        Returns:
          changes: 
          rows: 

        Raises:
          TypeError: sql argument must be either a string or a list.
          ValueError: sql_statement string must be a complete SQL statement.
          TypeError: If sql argument is a list, then items remaining in
              list after removal of sql_statement must be tuples.
          sqlite3.IntegrityError: NOT NULL constraint failed.
          sqlite3.IntegrityError: UNIQUE constraint failed.
          sqlite3.OperationalError: no such column or table.
          sqlite3.ProgrammingError: Cannot operate on a closed cursor or database.
          sqlite3.Warning: You can only execute one statement at a time.
          sqlite3.DatabaseError: File is encrypted or is not a database.

        """

        # Start execution of SQL statement(s).
        logging.info(('Starting execution of SQL statement(s) from '
                      'sql argument: {} : {}').format(id(sql),sql))

        # Check if sql argument is a string or a list. If sql argument 
        # is neither a string nor a list, then throw an exception. 
        logging.info('Type checking sql argument ...')
        try:
            if not (isinstance(sql, str) or isinstance(sql, list)):
                raise TypeError(('sql argument is NOT A STRING OR A '
                                 'LIST: {}').format(type(sql)))
        except TypeError as e:
            logging.exception(e)
            logging.debug('sql argument MUST BE A STRING OR A LIST.')
            raise
        else:
            logging.info(('sql argument is of type: '
                          '{}').format(type(sql)))

        # Determine execution mode for SQL statement(s). 
        logging.info('Determining execution mode for SQL '
                     'statement(s) ...')
        if isinstance(sql, str):
            if os.path.isfile(sql):
                execution_mode = 'SCRIPT' 
            else:
                execution_mode = 'NORMAL'
        elif isinstance(sql, list):
            execution_mode = 'MANY' 
        logging.info(('Execution mode is: {}').format(execution_mode))

        # Prepare SQL statement(s) based on execution mode.
        if execution_mode == 'NORMAL':
            logging.info('Copying SQL statement from string ...')
            sql_statement = sql
        elif execution_mode == 'MANY':
            logging.info('Removing SQL statement from list ...')
            sql_statement = sql.pop(0)
        elif execution_mode == 'SCRIPT':
            logging.info('Reading in SQL statement(s) from file ...')
            try:
                with open(sql, 'r') as sql_file:
                    sql_statement = sql_file.read()
            except Exception as e:
                logging.exception(e)
                raise
            else:
                logging.info(('SQL statement(s) have been read in from '
                              'file: {}'.format(sql)))

        # Check if sql_statement string is empty. If sql_statement
        # string is empty, then throw a warning.
        logging.info('Checking if sql_statement string is empty ...')
        try:
            if not sql_statement:
                raise ValueError('sql_statement string is EMPTY.')
        except ValueError as w:
            logging.warn(w)
        else:
            logging.info(('sql_statement string is not empty: '
                          '{}').format(sql_statement))

        # Check if sql_statement string is a complete SQL statement. If
        # sql_statement string is not a complete SQL statement, then 
        # throw an exception.
        logging.info('Checking if sql_statement string is a complete '
                     'SQL statement ...')
        try:
            if not sqlite3.complete_statement(sql_statement):
                raise ValueError('sql_statement string is NOT A '
                                 'COMPLETE SQL STATEMENT.')
        except ValueError as e:
            logging.exception(e)
            logging.debug('Check if the sql_statement string is '
                          'terminated by a semi-colon.')
            raise
        else:
            logging.info('sql_statement string is a complete SQL '
                         'statement.')

        # Perform execution mode-based checks on SQL statement(s) prior
        # to execution. For example, if execution mode is 'MANY', then 
        # before executing many SQL statements, check if all items 
        # remaining in the sql argument list are tuples.
        if execution_mode == 'MANY':
            logging.info('Type checking items remaining in the sql '
                         'argument list ...')
            try:
                for item in sql:
                    if not isinstance(item, tuple):
                        raise TypeError(('At least one item in the sql '
                                         'argument list is not a tuple: '
                                         '{}').format(type(item)))
            except TypeError as e:
                logging.exception(e)
                logging.debug('All items remaining in the sql argument '
                              'list should be a set of tuples that '
                              'represent the sequence of parameters to '
                              'execute against the SQL statement.')
                raise
            else:
                logging.info('All items remaining in the sql argument '
                             'list are tuples.')

        # Open a connection to database, create a cursor on this
        # connection, and then execute the SQL statement(s).
        try:
            with contextlib.closing(self.connect()) as connection:
                with connection:
                    logging.info('Creating a database cursor on the '
                                 'connection ...')
                    with contextlib.closing(connection.cursor()) as cursor:
                        logging.info(('cursor created: {}').format(cursor))
                        logging.info('Executing SQL statement(s) ...')
                        if execution_mode == 'NORMAL':
                            cursor.execute(sql_statement)
                        elif execution_mode == 'MANY':
                            cursor.executemany(sql_statement, sql)
                        elif execution_mode == 'SCRIPT':
                            cursor.executescript(sql_statement)
                        logging.info('SQL statement(s) executed.')
                        logging.info('Fetching any returned rows ... ')
                        rows = cursor.fetchall()
                        logging.info('Fetch complete.')
                        logging.info('Closing database cursor ...')
                    logging.info(('cursor closed: {}').format(cursor))
                logging.info('Saving the total number of database '
                             'rows that were modified, inserted, '
                             'and/or deleted during SQL statement '
                             'execution ...')
                changes = connection.total_changes
                logging.info('Closing database connection ...')
            logging.info(('connection closed: {}').format(connection))
        except Exception as e:
            logging.exception(e)
            raise
        else:
            logging.info(('Execution of SQL statement(s) complete: '
                          '{}').format(id(sql)))

        # Return the total number of database rows that were modified, 
        # inserted, and/or deleted by executing the SQL statement(s) 
        # AND any rows fetched from the database.
        return changes, rows


    def test(self):
        """ Run a test SQL query against the database.

        This method attempts to execute a test query against the 
        database to SELECT and fetch the names of the tables in the 
        database. 

        Arguments:
          None

        Returns:
          True or False: bool: If test query executes successfully, then 
              returns True. Otherwise, returns False.
        
        Raises:
          None

        """

        logging.info('Attempting to execute test SQL query against '
                     'database ...')
        try:
            changes, table_names = self.execute(
                """ SELECT name
                    FROM sqlite_master
                    WHERE type='table'
                    AND name!='sqlite_sequence'; """)
        except Exception as e:
            logging.exception(e)
            return False
        else:
            logging.info('Test SQL query executed successfully.')
            if not table_names:
                logging.warn('database contains no tables.')
                logging.debug('database needs a schema.')
            else:
                logging.info(('database table names are: '
                              '{}').format(table_names))
            return True


def main():

    # Set logging level.
    logging.basicConfig(level=logging.WARNING)

    # Create database object.
    db = SQLite3DB('example.db')

    # If database file does not exist, then create the database file by
    # executing the set of SQL statements that define the database's 
    # schema from a file. And once the database schema is loaded, load 
    # the initial data by executing a set of SQL statements from a file.
    if not os.path.isfile('example.db'):
       changes, rows = db.execute('example_db_schema.sql')
       changes, rows = db.execute('example_db_init.sql')

    # Run a test query on the database. 
    if db.test():
       print('Passed database test.')
    else:
       print('Failed database test.')
       return 1
    
    # Query the customer names from database.
    changes, rows = db.execute('SELECT name FROM customer;')
    print(changes, rows)
   
    # Add a merchant. Cooking Power Tools, LLC.
    changes, rows = db.execute("""
        INSERT INTO merchant ( name, country_id )
             SELECT 'Cooking Power Tools, LLC.', country.id
               FROM country
              WHERE country.name = 'United States'; 
        """)
    print(changes, rows)

    # Add a new product.
    changes, rows = db.execute("""
        INSERT INTO product ( merchant_id, name, price, status )
             SELECT merchant.id, 'Air Fryer', 99.95, 'Unavailble'
               FROM merchant
              WHERE merchant.name = 'Cooking Power Tools, LLC.';
        """)
    print(changes, rows)

    # Add a new order from a customer.
    changes, rows = db.execute("""
        INSERT INTO customer_order ( customer_id, status )
             SELECT customer.id, 'Pending'
               FROM customer
              WHERE customer.name = 'Rajneel';
        """)
    print(changes, rows)

    changes, rows = db.execute("""
        INSERT INTO order_item ( customer_order_id, product_id, quantity )
             VALUES ( ( SELECT customer_order.id
                          FROM customer_order
                         WHERE customer_order.customer_id =
                             ( SELECT customer.id
                                 FROM customer
                                WHERE customer.name = 'Rajneel' ) 
                           AND customer_order.status = 'Pending' ),
                             ( SELECT product.id
                                 FROM product
                                WHERE product.name='Air Fryer' ),
                             ( 1 ) ); 
        """)
    print(changes, rows)

    # Query what products each customer ordered and how many they ordered.
    changes, rows = db.execute("""
        SELECT customer.name, product.name, order_item.quantity
          FROM customer_order
          JOIN customer
            ON customer.id = customer_order.customer_id
          JOIN product 
            ON product.id = order_item.product_id
          JOIN order_item 
            ON customer_order.id = order_item.customer_order_id;
        """)
    print(changes, rows)

    return 0


if __name__ == '__main__':
    sys.exit(main())
