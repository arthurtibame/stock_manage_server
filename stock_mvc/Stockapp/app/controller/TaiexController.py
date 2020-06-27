from app import app
from app.service.TaiexService import get_taiex, update_taiex
from app.utils.auth import login_required 

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response

@app.route("/taiex", methods=["GET", "POST"])
@login_required
def taiex():
    taiexs = get_taiex()
    
    if request.method == 'GET':    
        print(session['cookie'])    
        return render_template('taiex.html', taiexs=taiexs)
    
    if request.method =="POST":   
        _ = update_taiex()
        if _ == '1': 
            taiexs = get_taiex()
            return render_template('taiex.html', taiexs=taiexs)
        else:
            return render_template('taiex.html', taiexs=taiexs, error_msg="1")

