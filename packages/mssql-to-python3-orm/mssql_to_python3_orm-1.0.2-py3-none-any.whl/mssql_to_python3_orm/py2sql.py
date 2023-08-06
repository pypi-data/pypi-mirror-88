import pyodbc

from mssql_to_python3_orm.base_db_info import BaseDbInfo


class Py2SQL:

    def __init__(self):
        self.connection_opened = False
        self.connection = None
        self.db = None
        self.cursor = None

    def db_connect(self, db: BaseDbInfo):
        if self.connection_opened:
            raise Exception('Current Py2SQL object already has an opened connection')
        self.db = db
        self.connection = pyodbc.connect(f'Driver={db.get_driver()};'
                                    f'Server={db.get_server()};'
                                    f'Database={db.get_db_name()};'
                                    f'Uid={db.get_user()};'
                                    f'Pwd={db.get_password()};')
        self.cursor = self.connection.cursor()
        self.connection_opened = True
        return self.connection

    def db_disconnect(self):
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None
        self.connection_opened = False
        self.db = None

    def db_engine(self):
        return 'MS SQL Server 2017'

    def db_engine_driver(self):
        return self.db.get_driver()

    def db_name(self):
        return self.db.get_db_name()

    def db_size(self):
        self.cursor.execute('EXEC sp_spaceused @oneresultset = 1')
        # database_name
        # database_size
        # unallocated space
        # reserved
        # data
        # index_size
        # unused
        for row in self.cursor:
            return row.database_size

    def db_tables(self):
        return self.cursor.tables(tableType='TABLE')

    def db_tables_names(self):
        return [x[2] for x in self.cursor.tables(tableType='TABLE')]

    def db_tables_info(self):
        return [f'1: {x[0]}; 2: {x[1]}; 3: {x[2]}; 4: {x[3]}; 5: {x[4]};' for x in self.db_tables()]

    def get_table(self, table_name):
        for table in self.db_tables():
            if table.table_name == table_name:
                return table

    def get_table_info(self, table_name):
        for table in self.db_tables():
            if table.table_name == table_name:
                return f'1: {table[0]}; 2: {table[1]}; 3: {table[2]}; ' \
                       f'4: {table[3]}; 5: {table[4]};'

    def db_table_structure(self, table):
        '''
        :param table: table name
        :return: list of tuples (id, name, type)
        id - column (attribute) number
        name - column (attribute) name
        type - column (attribute) data type name
        '''
        columns = []
        if not self.cursor.tables(table=table).fetchone():
           raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        # row[3] / row.column_name - column name
        # row[5] / row.type_name - column type
        # row[16] / row.ordinal_position - column id
        for row in self.cursor.columns(table=table):
            columns.append((row.ordinal_position, row.column_name, row.type_name))
        return columns

    def db_table_size(self, table):
        '''
        :param table: table name
        :return: the size of the db table as string
        '''
        if not self.cursor.tables(table=table).fetchone():
           raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        self.cursor.execute(f'sp_spaceused \'{self.__get_table_object_name__(table)}\'')

        # reserved = data + index_size + unused
        for row in self.cursor:
            return row.reserved

    def db_insert(self, table, values):
        if not self.cursor.tables(table=table).fetchone():
           raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        columns_info = self.db_table_structure(table)
        insert_query = f'insert into {self.__get_table_object_name__(table)}\n'
        insert_query += '('
        for i in range(len(columns_info)):
            # do not insert primary key
            if 'identity' in columns_info[i][2]:
                continue
            insert_query += columns_info[i][1]
            if i < len(columns_info) - 1:
                insert_query += ', '
        insert_query += ')\nvalues\n('
        for i in range(len(values)):
            # check type
            if type(values[i]) is int or type(values[i]) is float:
                insert_query += str(values[i])
            elif values[i] is None:
                insert_query += 'null'
            else:
                insert_query += f'\'{values[i]}\''
            if i < len(values) - 1:
                insert_query += ', '
        insert_query += ')'
        # for debug only
        #print(insert_query)
        self.cursor.execute(insert_query)
        self.cursor.commit()

    def get_table_foreign_keys(self, table):
        '''
        :param table: table that is referenced, NOT the one that references
        :return: full foreign keys info, see doc:
        https://github.com/mkleehammer/pyodbc/wiki/Cursor#foreignkeystablenone-catalognone-schemanone-foreigntablenone-foreigncatalognone-foreignschemanone
        '''
        if not self.cursor.tables(table=table).fetchone():
           raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        return self.cursor.foreignKeys(table)

    def __get_db_object_name__(self, table_schema, table_name):
        return f'[{table_schema}].[{table_name}]'

    def __get_table_schema_name__(self, table_name):
        return self.get_table(table_name).table_schem

    def __get_table_object_name__(self, table_name):
        return f'[{self.get_table(table_name).table_schem}].[{table_name}]'