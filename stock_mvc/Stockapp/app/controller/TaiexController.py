from app import app
from app.service.TaiexService import get_taiex, update_taiex
from app.utils.auth import login_required 

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response

@app.route("/taiex", methods=["GET", "POST"])
@login_required
def taiex():
    taiexs = get_taiex()    
    if request.method == 'GET':            
        return render_template('taiex.html', taiexs=taiexs)
    
    if request.method =="POST":   
        response_msg = update_taiex()
        if response_msg == '1': 
            taiexs = get_taiex()
            return render_template('taiex.html', taiexs=taiexs)
        elif response_msg == '今日已更新': 
            return render_template('taiex.html', taiexs=taiexs, response_msg=response_msg)
        else:
            response_msg = "請檢查目前時間是否正確"
            return render_template('taiex.html', taiexs=taiexs, response_msg=response_msg)

