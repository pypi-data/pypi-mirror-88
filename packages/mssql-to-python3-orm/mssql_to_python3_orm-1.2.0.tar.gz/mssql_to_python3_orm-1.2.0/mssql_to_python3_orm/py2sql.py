from datetime import datetime

import pyodbc

from mssql_to_python3_orm.base_db_info import BaseDbInfo

import inspect

class Py2SQL:

    def __init__(self):
        self.connection_opened = False
        self.connection = None
        self.db = None
        self.cursor = None

    def db_connect(self, db: BaseDbInfo):
        '''
        :param db: database to connect info
        :return: opened connection to db
        '''
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
        ''' Closes internal connection cursor and connection itself '''
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None
        self.connection_opened = False
        self.db = None

    def db_engine(self):
        '''
        :return: DBMS
        '''
        return 'MS SQL Server 2017'

    def db_engine_driver(self):
        '''
        :return: Current DBMS driver used
        '''
        return self.db.get_driver()

    def db_name(self):
        '''
        :return: Name of database which possesses active connection at the moment
        '''
        return self.db.get_db_name()

    def db_size(self):
        '''
        :return: Size of database which possesses active connection at the moment
        '''
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
        '''
        :return: all tables objects from internal cursor
        '''
        return self.cursor.tables(tableType='TABLE')

    def db_tables_names(self):
        '''
        :return: all table names
        '''
        return [x[2] for x in self.cursor.tables(tableType='TABLE')]

    def db_tables_info(self):
        '''
        :return: all tables info as strings collection
        '''
        return [f'1: {x[0]}; 2: {x[1]}; 3: {x[2]}; 4: {x[3]}; 5: {x[4]};' for x in self.db_tables()]

    def get_table(self, table_name):
        '''
        :param table_name: name of requested table
        :return: requested table object
        '''
        for table in self.db_tables():
            if table.table_name == table_name:
                return table

    def get_table_info(self, table_name):
        '''
        :param table_name: name of requested table
        :return: requested table info string
        '''
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
        '''
        Performs insert of an object consisting of values in table
        :param table: name of table to insert into
        :param values: values to insert (should be ordered as table's attributes, without primary)
        '''
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
        # print(insert_query)
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
        '''
        :return: [{table_schema}].[{table_name}]
        '''
        return f'[{table_schema}].[{table_name}]'

    def __get_table_schema_name__(self, table_name):
        '''
        :return: [{table_schema}].[{table_name}]
        '''
        return self.get_table(table_name).table_schem

    def __get_table_object_name__(self, table_name):
        '''
        :return: [{table_schema}].[{table_name}]
        '''
        return f'[{self.get_table(table_name).table_schem}].[{table_name}]'

    def get_table_primary_keys(self, table):
        '''
        :param table: table name
        :return: primary key constraints of table
        '''
        if not self.cursor.tables(table=table).fetchone():
            raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        self.cursor.execute('select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where '
                            f'TABLE_NAME = \'{table}\'')

        primary_keys = []
        for row in self.cursor:
            if row.CONSTRAINT_NAME.startswith('PK_'):
                primary_keys.append(row)

        return primary_keys

    def get_slave_table_foreign_keys(self, table):
        '''
        :param table: table name
        :return: foreign key constraints of table as a SLAVE table
        '''
        if not self.cursor.tables(table=table).fetchone():
            raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        self.cursor.execute('select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where '
                            f'TABLE_NAME = \'{table}\'')

        foreign_keys = []
        for row in self.cursor:
            if row.CONSTRAINT_NAME.startswith('FK_'):
                foreign_keys.append(row)

        return foreign_keys

    @staticmethod
    def to_py_type(db_type):
        '''
        :param db_type: type name from current db engine (MS SQL Server only)
        :return: appropriate python 3 type
        '''
        if 'int' in db_type:
            return int
        if 'char' in db_type or 'text' in db_type:
            return str
        if 'float' in db_type or 'numeric' in db_type or 'decimal' in db_type \
                or 'real' in db_type or 'money' in db_type:
            return float
        if 'flag' in db_type or 'bit' in db_type:
            return bool
        if 'Name' in db_type or 'Phone' in db_type or 'uniqueid' in db_type \
                or "varbinary" in db_type or 'xml' in db_type or 'time' in db_type:
            return str
        try:
            return globals()[db_type]
        except Exception:
            return None

    '''
    Classes methods
    '''

    def find_class(self, py_class):
        '''
        :param py_class: python 3 class
        :return: table structure appropriate to py_class
        '''
        attributes = inspect.getmembers(py_class, lambda a: not (inspect.isroutine(a)))
        attributes = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        for table in self.db_tables_names():
            table_structure = self.db_table_structure(table)
            found_attributes = 0
            for column in table_structure:
                name = column[1]
                db_type = column[2]
                py_type = Py2SQL.to_py_type(db_type)
                if not py_type:
                    break
                attribute_is_found = False
                for attribute in attributes:
                    if attribute[0] == name and type(attribute[1]) == py_type:
                        attribute_is_found = True
                        break
                if not attribute_is_found:
                    break
                found_attributes += 1
            if found_attributes == len(table_structure):
                return table_structure
        return None

    def find_classes_by(self, *attributes):
        table_structures = []
        for table in self.db_tables_names():
            table_structure = self.db_table_structure(table)
            found_attributes = 0
            for column in table_structure:
                name = column[1]
                db_type = column[2]
                py_type = Py2SQL.to_py_type(db_type)
                if not py_type:
                    break
                for attribute in attributes:
                    if attribute[0] == name and type(attribute[1]) == py_type:
                        found_attributes += 1
                        break
            if found_attributes == len(attributes):
                table_structures.append(table_structure)
        return table_structures

    def create_class(self, table, module):
        '''
        Generates source code of class appropriate to table in new module with name {module}.py
        :param table: table name
        :param module: module name (without ".py")
        '''
        table_structure = self.db_table_structure(table)
        class_src = f"class {table}:\n"
        for attribute in table_structure:
            name = attribute[1]
            py_type = Py2SQL.to_py_type(attribute[2])
            type_name = py_type.__name__
            if not type:
                return None
            class_src += f"\t{name} = {type_name}()\n"
        class_src += "\n"
        class_src += f"\tdef __init__(self, "
        for attribute in table_structure:
            name = attribute[1]
            py_type = Py2SQL.to_py_type(attribute[2])
            type_name = py_type.__name__
            class_src += f"{name}: {type_name}"
            if not attribute == table_structure[-1]:
                class_src += f", "
        class_src += "):\n"
        for attribute in table_structure:
            name = attribute[1]
            class_src += f"\t\tself.{name}={name}\n"
        class_src += "\n"

        class_file = open(module + '.py', 'w')
        class_file.write(class_src)
        class_file.close()

        demo_file = open('demo.py', 'r')
        demo_file.seek(0)
        demo_src = demo_file.read()
        demo_file.close()

        import_str = f"from {module} import {table}\n"

        if not import_str in demo_src:
            demo_src = import_str + demo_src
            demo_file = open('demo.py', 'w')
            demo_file.write(demo_src)
            demo_file.close()

    def find_object(self, table, py_object):
        if not self.cursor.tables(table=table).fetchone():
            raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        columns_info = self.db_table_structure(table)

        columns_info_type_names = []
        attributes_names = []

        for i in range(len(columns_info)):
            columns_info_type_names.append(columns_info[i][1])

        for item in py_object.__dict__:
            attributes_names.append(item)

        if not columns_info_type_names == attributes_names:
            raise Exception(f'Different attributes in {table} and object')

        select_query = f'select * from {self.__get_table_object_name__(table)} where '

        for i in range(len(columns_info_type_names)):
            value = py_object.__dict__[attributes_names[i]]

            if (value == 'None'):
                select_query += str(columns_info_type_names[i]) + ' is null'
            elif isinstance(value, str):
                select_query += str(columns_info_type_names[i]) + '=\'' + value + '\''
            elif (isinstance(value, datetime.datetime)):
                select_query += str(columns_info_type_names[i]) + '=\'' + str(value) + '\''
            else:
                select_query += str(columns_info_type_names[i]) + '=' + str(value)

            if not i == len(columns_info) - 1:
                select_query += ' and '

        select_query += ';'

        # for debug only
        # print(select_query)

        res = []
        cols = self.db_table_structure(table)

        for (id, name, type) in cols:
            res.append([name, type])

        self.cursor.execute(select_query)

        for row in self.cursor:
            for index in range(len(row)):
                res[index].append(row[index])

        # for debug only
        # print(res)

        return res

    def find_objects_by(self, table, *attributes):
        if not self.cursor.tables(table=table).fetchone():
            raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        columns_info = self.db_table_structure(table)

        columns_info_type_names = []

        for i in range(len(columns_info)):
            columns_info_type_names.append(columns_info[i][1])

        for atr in attributes:
            if not atr in columns_info_type_names:
                raise Exception(f'Invalid attributes')

        select_query = f'select '

        for i in range(len(attributes)):
            select_query += attributes[i]

            if not i == len(attributes) - 1:
                select_query += ', '
            else:
                select_query += ' '

        select_query += f'from {self.__get_table_object_name__(table)}'

        # for debug only
        # print(select_query)

        cols = self.db_table_structure(table)
        names_and_types = []
        res = []

        for (id, name, type) in cols:
            if name in attributes:
                names_and_types.append([name, type])

        self.cursor.execute(select_query)

        for row in self.cursor:
            temp = []
            for item in range(len(row)):
                temp.append([names_and_types[item][0], names_and_types[item][1], row[item]])
            res.append(temp)

        # for debug only
        # print(res)

        return res

    def create_object(self, table, id):
        if not self.cursor.tables(table=table).fetchone():
            raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        pk_column_name = ''

        for row in self.get_slave_table_primary_keys(table):
            pk_column_name = row[-2]

        select_query = f'select * from {self.__get_table_object_name__(table)} where {pk_column_name}={id}'

        # for debug only
        # print(select_query)

        self.create_class(table, table)
        imp = __import__(table, fromlist=[table])
        new_class = getattr(imp, table)

        self.cursor.execute(select_query)
        args = []

        for row in self.cursor:
            for arg in row:
                args.append(arg)

        if not len(args) == 0:
            return new_class(*args)

    def create_objects(self, table, fid, lid):
        if not self.cursor.tables(table=table).fetchone():
            raise Exception(f'Table {table} does not exist in db {self.db_name()}')

        if not isinstance(fid, int):
            raise Exception(f'fid must be int')

        if not isinstance(lid, int):
            raise Exception(f'lid must be int')

        if not fid < lid:
            raise Exception(f'fid must be less then lid')

        pk_column_name = ''

        for row in self.get_slave_table_primary_keys(table):
            pk_column_name = row[-2]

        select_query = f'with num_row as ( select row_number() over (order by {pk_column_name}) as nom, * from {self.__get_table_object_name__(table)}) select * from num_row where nom between {fid} and {lid};'

        # for debug only
        # print(select_query)

        self.create_class(table, table)
        imp = __import__(table, fromlist=[table])
        new_class = getattr(imp, table)

        self.cursor.execute(select_query)
        res = []

        for row in self.cursor:
            args = []
            for index in range(len(row)):
                if not index == 0:
                    args.append(row[index])
            if not len(args) == 0:
                res.append(new_class(*args))

        return res

