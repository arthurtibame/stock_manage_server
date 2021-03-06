from app import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from app.utils.auth import login_required
from app.utils.crawler import Crawler
from app.service.ChooseShortTermStrongStockService import insert_short_term_strong_stock



@app.route('/choose_short_term_strong_stock', methods=["GET", "POST"])
@login_required
def choose_short_term_strong_stock():
    test = ""
    content = ""
    contents = Crawler().short_term_strong_stock
    if request.method == "GET" :        
        
        if contents != None:
            return render_template('choose_short_term_strong_stock.html', contents=contents)
        else:
            #如果資料尚未更新 在前端顯示尚未更新
            contents = ""
            error_msg = "尚未更新"
            return render_template('choose_short_term_strong_stock.html', contents=contents, error_msg=error_msg)
        

    try:
        content = request.form['postback']
        
    except:
        pass

    if request.method == "POST" and content != test:
        
        res_msg = insert_short_term_strong_stock(content)
        return render_template('choose_short_term_strong_stock.html', contents=contents, res_msg = res_msg)

    return redirect(url_for('short_term_strong_stock'))

