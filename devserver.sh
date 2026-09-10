#!/bin/sh
source .venv/bin/activate
python -u -m flask --app main run -p $PORT --debug
pip install --update
pip install numpy pandas
pip install matplotlib seaborn
pip install scipy statsmodels
pip install scikit-learn
pip install dask matplotlib
pip install fire base
pip install flask
pip install flask-cors
pip install google-generativeai
pip install --upgrade firebase-admin google-cloud-firestore google-api-core
pip install -r requirements.txt
npm install update
export FIREBASE_WEB_API_KEY="AIzaSyCKKcD1NYxO_sJVevtwoHom95pNdAwLRUw"