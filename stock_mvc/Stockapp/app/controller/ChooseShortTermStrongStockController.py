from app import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from app.utils.auth import login_required
from app.utils.crawler import Crawler


@app.route('/choose_short_term_strong_stock', methods=["GET", "POST"])
@login_required
def choose_short_term_strong_stock():
    test = ""
    content = ""
    if request.method == "GET":
        contents = Crawler().short_term_strong_stock
        return render_template('choose_short_term_strong_stock.html', contents=contents)

    try:
        content = request.form['postback']
        
    except:
        pass

    if request.method == "POST" and content != test:
        #res_msg = callback(content)
        res_msg = ""
        contents = Crawler().short_term_strong_stock

        return render_template('choose_short_term_strong_stock.html', contents=contents, res_msg = res_msg)

    return redirect(url_for('short_term_strong_stock'))

