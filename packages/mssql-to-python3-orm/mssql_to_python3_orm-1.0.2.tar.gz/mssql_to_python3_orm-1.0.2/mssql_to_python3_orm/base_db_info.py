class BaseDbInfo:
    def __init__(self,
                 db_name = 'TestDatabase',
                 uid = 'ormserveruser',
                 pwd = 'pa$$w0rd',
                 driver = '{ODBC Driver 17 for SQL Server}',
                 server = 'tcp:test-server-orm.database.windows.net,1433'):
        self.__driver = driver
        self.__server = server
        self.__db_name = db_name
        self.__uid = uid
        self.__pwd = pwd

    def get_db_name(self):
        return self.__db_name

    def get_driver(self):
        return self.__driver

    def get_server(self):
        return self.__server

    def get_user(self):
        return self.__uid

    def get_password(self):
        return self.__pwd