from app import app
from app.service.ShortTermStrongStockService import get_short_term_strong_stock
from app.utils.auth import login_required 

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response,Response

@app.route('/short_term_strong_stock', methods=["GET", "POST"])
@login_required
def short_term_strong_stock():
    short_term_strong_stocks = get_short_term_strong_stock()
    
    if request.method =="GET":        
        return render_template('short_term_strong_stock.html', short_term_strong_stocks = short_term_strong_stocks)
    
    else:
        
        return redirect(url_for('choose_short_term_strong_stock'))