from app import app
from app.utils.auth import login_required, request_user

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response

####  setup routes  ####
@app.route('/')
@login_required
def index():
    return render_template('index.html')#, user = user_label)


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear the inital flash message
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    # query the user
    json_content = request_user(username, password)
    statusCode = json_content["statusCode"]
    
    
    print(statusCode)
    if request.method == 'POST':
        if statusCode == 200:
            
            #global user_label
            #user_label = json_content['data']['Name']    

            #session['cookie'] = bytes(json_content['data']['ID'])
            #session['username'] = request.form['username']
            session['cookie'] = json_content['data']['Key']
            print("Keys:    ",json_content['data']['Key'])
            print("Cookie:  ",session['cookie'])
            return redirect(url_for('index'))            
        else:
            return render_template('login.html' ,error_msg = json_content["message"])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


    

