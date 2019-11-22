from flask import Flask, render_template

from views import views


app = Flask(__name__)
app.register_blueprint(views)
