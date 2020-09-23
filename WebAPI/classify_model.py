import numpy as np
import xgboost as xgb
from joblib import dump,load
from WebAPI.views import write_anomaly
def predict(data):
    data = np.array(data)
    #当特征的数量发生变化时，这里也需要相应的改变
    data1 = data[:,2:20]
    data2 = data[:,22:40]
    data_train = np.concatenate((data1,data2),axis=1)
    data_train = data_train.astype("float32")

    xg_test = xgb.DMatrix(data_train)
    # xg_test = data_train

    class_2 = load('WebAPI/class_2.pkl')
    anomaly = class_2.predict(xg_test)
    anomaly = (anomaly >= 0.5) * 1

    class_n = load('WebAPI/class_n.pkl')
    probas = class_n.predict(xg_test)

    for i in range(len(data)):
        if( anomaly[i] == 1 or anomaly[i] == '1'):
            rid = int(data[i][20])
            time = data[i][21]
            event = np.argmax(probas[i])
            prob_1 = probas[i][0]
            prob_2 = probas[i][1]
            prob_3 = probas[i][2]
            prob_4 = probas[i][3]
            prob_5 = probas[i][4]
            prob_6 = probas[i][5]
            write_anomaly(rid,time,event,prob_1,prob_2,prob_3,prob_4,prob_5,prob_6)

