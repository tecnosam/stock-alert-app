from setuptools import setup

setup(
   name='OPENSTOCK',
   version='1.0',
   description='App that helps you watch the stock market',
   author='Abolo Samuel',
   author_email='ikabolo59@gmail.com',
   packages=['openstock'],  #same as name
   install_requires=['gunicorn', 'yfinance', 'flask-socketio', 'flask', 'numpy', 'flask-cors', 'pandas', 'pymysql'], #external packages as dependencies
)
