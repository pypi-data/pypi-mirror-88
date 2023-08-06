
class PostgresTools:
    def __init__(self, user, key, host, port, base, schema='public'):
        self.user = str(user)
        self.key = str(key)
        self.host = str(host)
        self.port = str(port)
        self.base = str(base)
        self.schema = schema
        self.engine = sa.create_engine('postgresql://' + user + ':' + key + '@' + host + ':' + port + '/' + base)
        
    
    def pd_log(self, lisEvent, table_log = 'log_soma'):
        self.table_log = table_log
        pd_log = pd.DataFrame(np.array(lista).transpose(), columns=['date_r', 'description'])
        pd_log.to_sql(
                name=self.table_log, # database table name
                con=self.engine,
                if_exists='append',
                index=False
                )
        
    def readtables(self):
        #self.schema = schema
        self.tables = pd.DataFrame(self.engine.execute("SELECT table_name FROM information_schema.tables where table_schema = '{}' and table_type = 'BASE TABLE'".
                                                  format(self.schema)).fetchall(), columns=['table']).table.unique()
    
        return self.tables
        
        
    def readcolumns(self, table):
        self.table = table
        self.columns_data = pd.DataFrame(self.engine.execute("select column_name from information_schema.columns where table_name = '{}'".
                                                   format(self.table)).fetchall(), columns=['col']).col.unique()
        return self.columns_data
        
        
    def readdata(self, table, limit=2000000):
        self.table = table
        self.limit = limit
        
        self.columns = pd.DataFrame(self.engine.execute("select column_name from information_schema.columns where table_name = '{}'".
                                                        format(self.table)).fetchall(), columns=['col']).col.unique()
        
        self.dataset = pd.DataFrame(self.engine.execute('select * from "{}".{}'.format(self.schema, self.table)).fetchall(), columns=self.columns)
        
        print('select * from "{}".{} limit {}'.format(self.schema, self.table, self.limit))
        return self.dataset
    
    
    def writetable(self, dataset, table, argument = 'replace'):
        self.argument = argument
        self.dataset = dataset
        self.table = table
        self.dataset.to_sql(name=self.table, # database table name
                            con=self.engine,
                            if_exists=self.argument,
                            index=False
                            )
        
        
    
