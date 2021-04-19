from ext.utils import *
import sys, os, math
from db.mysql import Connection
import numpy as np
import pandas as pd
from datetime import datetime as dt

class TradingConditions:
	def __init__(self):
		self.db = Connection()
	def change(self, uid, name, node, val):
		check = f"SELECT * FROM trade WHERE `uid`={uid} AND `name`=\'{name}\'"
		# edit
		if ( self.db.check( check ) == True ):
			sql = f"UPDATE trade SET `%s`={val} WHERE `uid`={uid} AND `name`='%s'" % (node, name)
			a = self.db.set( sql )
			if (a == True):
				return True
			return False
		# add new stock
	def add_item(self, uid, name, open_, close, high, low, dividends, splits):
		check = f"SELECT * FROM trade WHERE `uid`={uid} AND `name`=\'{name}\'"
		if (self.db.check( check ) == False):
			sql = """
						INSERT INTO trade 
						(`uid`, `name`, `open`, `close`, `high`, `low`, `dividends`, `splits`)
						VALUES
						(%s, '%s', %s, %s, %s, %s, %s, %s)
					""" % ( uid, name.lower(), open_, close, high, low, dividends, splits )
			res = self.db.set( sql )
			if (res == True):
				return True
			else:
				print( "Res: ",res )
				return res
		else:
			return -2
		return False
	def check(self, uid, name='*'):
		if ( name == '*' ):
			sql = f"SELECT * FROM trade WHERE `uid`={uid}"
			dt = self.db.get( sql )
			conditions = []
			for i in dt:
				conditions.append({
				'id': i[0],
				'uid': i[1],
				'name': i[2].upper(),
				'open': i[3],
				'close': i[4],
				'high': i[5],
				'low': i[6],
				'dividends': i[7],
				'splits': i[8]
			})
			return conditions
		else:
			sql = f"SELECT * FROM trade WHERE `uid`={uid} AND `name`=\'{name}\'"
			dt = self.db.get( sql )[0]
			return {
				'id': dt[0],
				'uid': dt[1],
				'name': dt[2].upper(),
				'open': dt[3],
				'close': dt[4],
				'high': dt[5],
				'low': dt[6],
				'dividends': dt[7],
				'splits': dt[8]
			}
		return None
	def bidders(self, name):
		sql = f"SELECT 	`uid`,`open`,`close`,high,low,dividends,splits FROM trade WHERE `name`='%s'" % name
		res = self.db.get(sql)
		return pd.DataFrame( res, 
		 columns = ['uid', 'Open', 'Close', 'High', 'Low', 'Dividends', 'Splits'] 
		)
	def del_item(self, _id):
		sql = f"DELETE FROM trade WHERE id={_id}"
		return self.db.set( sql )

class SellingConditions:
	def __init__(self):
		self.db = Connection()
	def change(self, uid, name, node, val):
		check = f"SELECT * FROM sell WHERE `uid`={uid} AND `name`=\'{name}\'"
		# edit
		if ( self.db.check( check ) == True ):
			sql = f"UPDATE sell SET `%s`={val} WHERE `uid`={uid} AND `name`='%s'" % (node, name)
			a = self.db.set( sql )
			if (a == True):
				return True
			return False
		# add new stock
	def add_item(self, uid, name, open_, close, high, low, dividends, splits):
		check = f"SELECT * FROM sell WHERE `uid`={uid} AND `name`=\'{name}\'"
		if (self.db.check( check ) == False):
			sql = """
						INSERT INTO sell 
						(`uid`, `name`, `open`, `close`, `high`, `low`, `dividends`, `splits`)
						VALUES
						(%s, '%s', %s, %s, %s, %s, %s, %s)
					""" % ( uid, name.lower(), open_, close, high, low, dividends, splits )
			res = self.db.set( sql )
			if (res == True):
				return True
		else:
			return -2
		return False
	def check(self, uid, name='*'):
		if ( name == '*' ):
			sql = f"SELECT * FROM sell WHERE `uid`={uid}"
			dt = self.db.get( sql )
			conditions = []
			for i in dt:
				conditions.append({
				'id': i[0],
				'uid': i[1],
				'name': i[2].upper(),
				'open': i[3],
				'close': i[4],
				'high': i[5],
				'low': i[6],
				'dividends': i[7],
				'splits': i[8]
			})
			return conditions
		else:
			sql = f"SELECT * FROM sell WHERE `uid`={uid} AND `name`=\'{name}\'"
			dt = self.db.get( sql )[0]
			return {
				'id': dt[0],
				'uid': dt[1],
				'name': dt[2].upper(),
				'open': dt[3],
				'close': dt[4],
				'high': dt[5],
				'low': dt[6],
				'dividends': dt[7],
				'splits': dt[8]
			}
		return None
	def bidders(self, name):
		sql = f"SELECT 	`uid`,`open`,`close`,high,low,dividends,splits FROM sell WHERE `name`='%s'" % name
		res = self.db.get(sql)
		return pd.DataFrame( res, 
		 columns = [ 'uid', 'Open', 'Close', 'High', 'Low', 'Dividends', 'Splits'] 
		)
	def del_item(self, _id):
		sql = f"DELETE FROM sell WHERE id={_id}"
		return self.db.set( sql )


class BuyingConditions:
	def __init__(self):
		self.db = Connection()
	def change(self, uid, name, node, val):
		check = f"SELECT * FROM buy WHERE `uid`={uid} AND `name`=\'{name}\'"
		# edit
		if ( self.db.check( check ) == True ):
			sql = f"UPDATE buy SET `%s`={val} WHERE `uid`={uid} AND `name`='%s'" % (node, name)
			a = self.db.set( sql )
			if (a == True):
				return True
			return False
		# add new stock
	def add_item(self, uid, name, open_, close, high, low, dividends, splits):
		check = f"SELECT * FROM buy WHERE `uid`={uid} AND `name`=\'{name}\'"
		if (self.db.check( check ) == False):
			sql = """
						INSERT INTO buy 
						(`uid`, `name`, `open`, `close`, `high`, `low`, `dividends`, `splits`)
						VALUES
						(%s, '%s', %s, %s, %s, %s, %s, %s)
					""" % ( uid, name.lower(), open_, close, high, low, dividends, splits )
			res = self.db.set( sql )
			if (res == True):
				return True
			else:
				print( "RES: ", res )
				return res
		else:
			return -2
		return False
	def check(self, uid, name='*'):
		if ( name == '*' ):
			sql = f"SELECT * FROM buy WHERE `uid`={uid}"
			dt = self.db.get( sql )
			conditions = []
			for i in dt:
				conditions.append({
					'id': i[0],
					'uid': i[1],
					'name': i[2].upper(),
					'open': i[3],
					'close': i[4],
					'high': i[5],
					'low': i[6],
					'dividends': i[7],
					'splits': i[8]
			})
			return conditions
		else:
			sql = f"SELECT * FROM buy WHERE `uid`={uid} AND `name`=\'{name}\'"
			dt = self.db.get( sql )[0]
			return {
				'id': dt[0],
				'uid': dt[1],
				'name': dt[2].upper(),
				'open': dt[3],
				'close': dt[4],
				'high': dt[5],
				'low': dt[6],
				'dividends': dt[7],
				'splits': dt[8]
			}
		return None
	def bidders(self, name):
		sql = f"SELECT `uid`,`open`,`close`,high,low,dividends,splits FROM buy WHERE `name`='%s'" % name
		res = self.db.get(sql)
		return pd.DataFrame( res, 
		 columns = ['uid', 'Open', 'Close', 'High', 'Low', 'Dividends', 'Splits'] 
		)
	def del_item(self, _id):
		sql = f"DELETE FROM buy WHERE id={_id}"
		return self.db.set( sql )

def fetch_user_data(uid):
	sql = f"SELECT * FROM users WHERE id={uid}"
	db = Connection()
	res = db.get( sql )[0]
	return res

def reactivate_usr( uid ):
	sql = f"UPDATE users SET `activation`=now() WHERE `uid`={uid}"
	db = Connection()
	try:
		res = db.set( sql )
	except:
		res = db.set( sql )
	return res

def compute_activated(x):
    y = pd.to_datetime( dt.now() )
    z = y-x
    if ( z.days < 31 ):
        return True
    return False


# obj = SellingConditions()
# print( "Add item to watchlist: ",  obj.add_item( 1, 'PEPPER', 13, 14, 16, 13, 12000, 0.8, 0.56 ))
# print("Bidders: \n", obj.bidders( 'PEPPER' ))
# print("Bidders: \n", obj.bidders( 'GOLD' ))
# print( "Add item to watchlist: ",  obj.add_item( 1, 'DANGOTE', 4, 13, 19, 2, 12000 ))
# print( "Change items watchlist setting. reducing open price from 8 to 14: ", \
# 	obj.change( 2, 'GOLD', 'open', 14 ) )
# print( "Checking all items: ", obj.check( 1 ) )