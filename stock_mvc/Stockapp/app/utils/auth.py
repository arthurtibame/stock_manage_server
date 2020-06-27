from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import json

# Decorator Function
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if "cookie" in session:
            return func(*args, **kwargs)
        else:
            flash("\"You shall not pass!\" - Gandalf")
            return redirect(url_for("login"))
    return wrap

def request_user(account, password):
    
    url = 'http://zhix6842.ga:5000/api/user/login'
    raw = {
        "Account": str(account),
        "Password": str(password)
    }
    res = requests.post(url, json=raw)
    json_content = json.loads(res.text)
    return json_content
    """
    zhix6842@gmail.com
    sam123456
    """