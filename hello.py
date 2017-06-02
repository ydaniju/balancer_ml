from numpy import genfromtxt
import numpy as np
import statsmodels.api as sm



def apparent_power(active, reactive):
    import numpy as np
    return np.sqrt(np.add(np.square(active), np.square(reactive)))


my_data = genfromtxt('turbines.csv', delimiter=',', names=True)
active = my_data['ACTIVE_POWER']
reactive = my_data['REACTIVE_POWER']

y = apparent_power(active, reactive)

x = [
     my_data['WIND_DIRECTION'],
     my_data['WIND_SPEED'],
     my_data['HYDRAULIC_OIL_TEMP'],
     my_data['AMBIENT_TEMP'],
     my_data['TURBINE_STATUS']
    ]

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results.params

"""Cloud Foundry test"""
from flask import Flask
from flask import jsonify

import os

app = Flask(__name__)

port = int(os.getenv('VCAP_APP_PORT', '8080'))

@app.route('/')
def hello_world():
    result = reg_m(y, x).tolist()
    res_arr = [
        {
            "windDirection": result[0],
            "windSpeed": result[1],
            "hydraulicOilTemp": result[2],
            "ambientTemp": result[3],
            "turbineStatus": result[4],
            "expectedApparentPower": result[5]
        }
    ]
    return jsonify(res_arr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
