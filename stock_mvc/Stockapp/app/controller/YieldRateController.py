from app import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from app.utils.auth import login_required
from app.service.YieldRateService import callback
from app.utils.crawler import Crawler


@app.route('/yield_rate', methods=["GET", "POST"])
@login_required
def yield_rate():
    test = ""
    content = ""
    if request.method == "GET":
        contents = Crawler().yield_rate
        return render_template('yield_rate.html', contents=contents)

    try:
        content = request.form['postback']
        
    except:
        pass

    if request.method == "POST" and content != test:
        res_msg = callback(content)
        contents = Crawler().yield_rate

        return render_template('yield_rate.html', contents=contents, res_msg = res_msg)

    return redirect(url_for('today_stock'))
    # if request.method =="POST":
    #    contents = Crawler().yield_rate
    #    return render_template('yield_rate.html', contents = contents)
    #    #return redirect(url_for('index'))
