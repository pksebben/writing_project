from flask import Flask, render_template, session

from views import views

app = Flask(__name__)
app.secret_key="kcubaiebfkjsdliausdbf"
app.register_blueprint(views)
# app.register_blueprint(interface)
