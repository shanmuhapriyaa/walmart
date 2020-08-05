import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
#from sklearn.externals import joblib


app = Flask(__name__)

# load the model from disk

# REg
model = pickle.load(open('model.pkl', 'rb'))
modelE=pickle.load(open('modelE.pkl','rb'))
# Classification
clf = pickle.load(open('nlp_model.pkl', 'rb'))
cv = pickle.load(open('tranform.pkl', 'rb'))

sales_r=pickle.load(open('Pickle_RL_Model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/predict', methods=['POST'])
def predict_sales():

    format = request.args.get('format')

    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print(final_features)
    df = pd.DataFrame(final_features, columns=['Store',	'Dept',	'isHoliday',	'Size',	'Temperature',	'MarkDown1',	'MarkDown2',	'MarkDown4',	'MarkDown5',	'Type_A',	'Type_B',	'Type_C',	'Month'])

    #df=pd.DataFrame(final_features,columns=['Store','Dept','Date','IsHoliday','Size','Temperature','Fuel_Price','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','Unemployment','Type_A','Type_B','Type_C','Month','Year','Week'])
    prediction = sales_r.predict(df)
    print(prediction)

    output = prediction

    if(format == 'json'):
        return jsonify({'predict_sales': int(output)})

    return render_template('result.html', prediction_text='Sales prediction should be $ {}'.format(output))



@app.route('/predict', methods=['POST'])
def predict():
     json_ = request.json
     query_df = pd.DataFrame(json_)
     query = pd.get_dummies(query_df)
     prediction = clf.predict(query)
     render_template('result.html', prediction_text='Sales prediction should be $ {}'.format(output))

if __name__ == '__main__':

     app.run(port=8080)



# auto-reload on code change
