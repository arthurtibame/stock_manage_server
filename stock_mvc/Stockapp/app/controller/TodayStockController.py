from app import app,db 
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from app.utils.auth import login_required

from app.service.TodayStockService import get_today_stock

@app.route('/today_stock', methods=["GET", "POST"])
@login_required
def today_stock():
    today_stocks = get_today_stock()
    if request.method =="GET":        
        return render_template('today_stock.html', today_stocks = today_stocks)
    else:
        today_stocks = get_today_stock()
        return redirect(url_for('yield_rate'))
