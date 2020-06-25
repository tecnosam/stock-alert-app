from flask import *
from flask_socketio import SocketIO, emit, send
import numpy as np
import pandas as pd
import api, account_api
from watch import Watch
import stripe
import os
from datetime import datetime as dt

app = Flask(__name__)

Watch()

app.secret_key = b"$_JIL_-"
sock = SocketIO(app)

pub_key = 'pk_test_PX8gQIxfzI6HvZPODMzhAQlt00xMOZRz4z'

stripe.api_key = 'sk_test_6iiKSV7F68X3AvRGPf32l2p300y05YslWf'

s_l = pd.read_csv("stocks.csv")

def compute_activated(x):
    y = pd.to_datetime( dt.now() )
    z = y-x
    if ( z.days < 31 ):
        return True
    return False

@app.errorhandler(404)
def _404(err):
    return redirect( url_for("login") )

# @app.route("/")
# def base():
#     if ('uid' not in session):
#         return redirect( url_for( "login" ) )
#     return render_template("html/base.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        dat = request.form
        obj = account_api.User()
        res = obj.login( **dat )
        if (res != False):
            session['uid'] = res[0]
            session['name'] = res[1]
            session['email'] = res[2]
            session['pwd'] = dat['pwd']
            act = pd.to_datetime(res[4])
            session['activation'] = compute_activated( act )
            return redirect( url_for( "view", func = "buying" ) )
        else:
            flash("Oops, Your email or password is incorrect please try again0", "danger")
        return redirect( url_for( "login" ) )
    return render_template( "html/login.html" )

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if ( request.method == 'POST' ):
        dat = request.form
        if (dat['pwd'] != dat['re_pass']):
            flash( "Passwords do not match2", "warning" )
            return redirect( url_for('signup') )
        res = account_api.User().create( dat['name'], dat['email'], dat['pwd'] )
        if (res == True):
            flash("Account created successfully, you can now login with your new user1", "success")
            return redirect( url_for("login") )
        elif (res == -2):
            flash( "A user with this email already exists2", "warning" )
        else:
            flash( "Something went wrong please try again later0", "danger" )
        return redirect( url_for('signup') )
    return render_template( "html/signup.html" )

@app.route("/edit/usr", methods = ['POST'])
def edit_usr():
    if ( 'uid' not in session ):
        abort(404)
    cred = request.form
    obj = account_api.User()
    for i in cred:
        if ( session[i] == cred[i] ):
            continue
        res = obj.ChangeAttr( i, cred[ i ], session['uid'] )
        if ( res == True ):
            session[ i ] = cred[i]
        elif ( res == -2 ):
            flash( f"Could not change your {i} because its been taken by someone else", "warning" )
    return redirect( url_for( "view", func = "buying" ) )

@app.route("/view/<func>")
def view(func):
    if ('uid' not in session):
        return redirect( url_for("login") )
    if (func == 'buying'):
        obj = api.BuyingConditions()
    elif (func == 'selling'):
        obj = api.SellingConditions()
    elif (func == 'curious'):
        obj = api.TradingConditions()
    else:
        return redirect(url_for("login"))
    stocks = obj.check( session['uid'] )
    return render_template("html/data_renderer.html", pub_key = pub_key, s_l = s_l, stocks = stocks, func = func)

@app.route("/add/<type_>", methods = ['POST'])
def add_cond(type_):
    if ('uid' not in session):
        return redirect( url_for("login") )
    if (type_ == 'buying'):
        obj = api.BuyingConditions()
    elif (type_ == 'selling'):
        obj = api.SellingConditions()
    elif ( type_ == 'curious' ):
        obj = api.TradingConditions()
    else:
        abort(404)
    dat = dict(request.form)
    dat['uid'] = session['uid']
    dat['open_'] = dat.pop("open")
    res = obj.add_item( **dat )
    if ( res == True ):
        flash( "Created successfully", "success" )
        # return redirect( url_for("") )
    elif (res == -2):
        flash( f"You've already added a {type_} watcher for this ticker.", "warning" )
    else:
        print("\n\n%s" % res)
        flash("That didnt work. My bad, please try again later while we try to resolve this", "danger")
    return redirect( url_for('view', func = type_) )


@app.route("/edit/<klass>/<symb>", methods = ['POST'])
def edit_watcher(klass, symb):
    if ( 'uid' not in session ):
        abort(404)
    if ( klass == 'curious' ):
        obj = api.TradingConditions()
    elif ( klass == 'buying' ):
        obj = api.BuyingConditions()
    elif (klass == 'selling'):
        obj = api.SellingConditions()
    else:
        abort(404)
    cred = request.form
    for i in cred:
        res = obj.change( session['uid'], symb, i, cred[ i ] )
        if ( res == True ):
            continue
    
    return redirect( url_for( "view", func = klass ) )

@app.route("/logout")
def logout():
    pops = [i for i in session]
    for i in pops:
        session.pop(i)
    return redirect(url_for("login"))

@sock.on("del-watcher")
def del_watcher(data):
    if (data['klass'] == 'buying'):
        obj = api.BuyingConditions()
    elif ( data['klass'] == 'selling' ):
        obj = api.SellingConditions()
    elif ( data['klass'] == 'cur' ):
        obj = api.TradingConditions()
    else:
        abort(404)
    dat = obj.del_item( data['_id'] )
    emit( "del-watcher", data, broadcast = True )

@app.route("/pay", methods = ['POST'])
def pay():
    customer = stripe.Customer.create( email=request.form['stripeEmail'], source=request.form['stripeToken'] )

    charge = stripe.Charge.create(
        customer = customer.id,
        amount = 3000,
        currency = 'usd',
        description = 'OPENSTOCK Alert service renewal for user %s ' % session['name']
    )
    api.reactivate_usr( session['uid'] )
    flash( "Process complete1", "success" )

    return redirect( url_for('logout') )

if __name__ == "__main__":
    sock.run( app, debug = True, host = '0.0.0.0' )