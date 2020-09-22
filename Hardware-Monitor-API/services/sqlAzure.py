# import sql.connector
import pyodbc

class Sql:
    def __init__(self, user, password, port, database, server):
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.server = server
        self.sql = None
        self.cursor = None

    #Estabelecendo uma conexão
    def connect(self):
        try:
            self.sql = pyodbc.connect(

                'DRIVER={ODBC Driver 17 for SQL Server}'+';SERVER='+self.server
                +';PORT='+self.port+';DATABASE='+self.database+';UID='+self.user+';PWD='+ self.password

            )
            #Criando cursor para manipulação do banco.
            print(self.sql)
            self.cursor = self.sql.cursor()
        except Exception as err:
            print(err)
            raise

    def insert(self, data):
        query = (
           
            "INSERT INTO dados_hw (cpu_percent, ram_percent, disk_percent, download, upload, temp_celsius, swap_percent, tasks) VALUES (?, ?, ?, ?, ?, ?, ?, ?)" 
        )
        values = data
        try:
            print('Inserindo Valores')
            self.cursor.execute(query,values)

            self.sql.commit()
        except Exception as err:
            print(err)
            self.sql.rollback()
            self.close()
    
    # Fechando conexão
    def close(self):
        self.sql.close()

        

