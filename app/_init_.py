import os
import firebase_admin
from firebase_admin import credentials
from flask import flask
def create_app():
    app = flask(__name__, template_folder='../static')
    app.secret_key = 'super_secret_key'
    
    try:
        if not firebase_admin._apps:
            try:
                cred = credentials.certificate("serviceaccountkey.json")
                firebase_admin.initialize_app(cred)
            except exception:
                firebase_admin.initialize_app()
            except exception as e:
                print("atenção: firebase não foi localizado corretamente.", e)
                
                from app,controllers.home_controller import home_bp
                from aoo.controllers.auth_controller import auth_bp
                
                app.register_blueprint(home_bp)
                app.register_blueprint(auth_bp)
                
                return app