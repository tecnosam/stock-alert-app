import pymysql as DBAdapter
import sys, os

class Connection:
    def __init__(self, 
        host = 'nnmeqdrilkem9ked.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', 
        usr = 'zamylucdxp90omle', pwd = 'nyg7yxh6ecs90w9k', db = "lk8ls4vwvv7rl3ic"):
        self.db = DBAdapter.connect( host, usr, pwd, db )
        #self.db = DBAdapter.connect( "localhost", "root", "", "openstock" )
    
    def set( self, sql ):
        with self.db.cursor() as c:
            try:
                c.execute( sql )
                self.db.commit()
                return True
            except DBAdapter.err.IntegrityError:
                return -2
            except Exception as e:
                self.db.rollback()
                raise e
        return False
    
    def get( self, sql ):
        with self.db.cursor()as c:
            try:
                c.execute( sql )
                res = c.fetchall()
                return res
            except Exception as e:
                raise e
        return ()
    def check( self, sql ):
        with self.db.cursor()as c:
            try:
                c.execute( sql )
                res = c.fetchall()
                return True if len(res) > 0 else False
            except Exception as e:
                raise e
        return False