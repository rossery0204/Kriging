from numpy import mean
from pykrige.ok import OrdinaryKriging
import Kriging
import General
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import math
import numpy as np


# INPUT: \
#     Thời gian bắt đầu: \ 
#         2008-07-01T11:00:00.000 \
#     Thời gian kết thúc: \
#         2008-12-31T11:00:00.000 \
#     Vĩ độ (TP Huế): \
#         16.47824423645664 \
#     Kinh độ (TP Huế): \
#         107.57367886624145 \
#     Bán kính tối đa: \
#         10 \
#     Cường độ tối thiểu: \
#         2


#build Kriging Estimator Model
class KrigingEstimator:
    
    def __init__(self, variogram_model):
        self.variogram_model = variogram_model

    def predict(self, X_val, X_tr, y_tr):
        pred = []
        var = []
        
        OK = OrdinaryKriging( X_tr[:,0],
                              X_tr[:,1],
                              y_tr,      
                              variogram_model=self.variogram_model,
                              verbose=True,
                              enable_plotting=False,
                              nlags = len(X_tr[:,0]))
        z_value, variance = OK.execute('grid', X_val[:,0], X_val[:,1])
        print("z value = ", z_value)
        for i in range (len(X_val[:,0])):
            pred.append(z_value[i][i])
            var.append(variance[i][i])
        print("pred = ", pred)
        print("var = ", var)
        return pred, var

def cross_validate(variogram_model, event):
    OK = Kriging.Kriging(variogram_model, event)
    lats, lons, data = OK.input_validate()
    print("lats = ", lats)
    print("lons = ", lons)
    print("data = ", data)

    #define features, target
    X = np.vstack((lons, lats)).T
    y = np.array(data)
    print("X = ", X)
    print("y = ", y)

    #define cross-validation method to use
    tscv = TimeSeriesSplit()

    me = [] #Mean Error
    rmse = [] #Root Mean Square Error
    ase = [] #Average Standardized Error
    mse = [] #Mean Standardized Error
    rmsse = [] #Root Mean Standardized Error

    fold = 0
    for train_idx, val_idx in tscv.split(X, y):
        X_tr = X[train_idx]
        y_tr = y[train_idx]
        print("X_tr = ", X_tr)
        print("y_tr = ", y_tr)
        
        X_val = X[val_idx]
        y_val = y[val_idx]
        
        print("X_val = ", X_val)
        print("y_val = ", y_val)

        kem = KrigingEstimator(variogram_model)
        pred, var = kem.predict(X_val, X_tr, y_tr)
        print("pred = ", pred)
        
        print(f"======= Fold {fold} ========")    
        me_score = mean(pred) - mean(y_val)
        print(f"ME is {me_score:0.6f} ")
        
        rmse_score = math.sqrt(mean_squared_error(y_val, pred))
        print(f"RMSE is {rmse_score:0.6f} ")
        
        ase_score = math.sqrt(mean(var))
        print(f"AMSE is {ase_score:0.6f}")
        
        inv_sqrt_var = []
        for i in range (len(var)):
            inv_sqrt_var.append(1 / float(math.sqrt(var[i])))
            
        element = []
        for i in range (len(var)):
            element.append(float((pred[i] - y_val[i]) * inv_sqrt_var[i]))
        
        mse_score = mean(element)
        print(f"MSE is {mse_score:0.6f}")
        
        element = []
        for i in range (len(var)):
            element.append(float(((pred[i] - y_val[i]) * inv_sqrt_var[i]))**2)
        
        rmsse_score = math.sqrt(mean(element))
        print(f"RMSSE is {rmsse_score:0.6f}")
        
        me.append(me_score)
        rmse.append(rmse_score)
        ase.append(ase_score)
        mse.append(mse_score)
        rmsse.append(rmsse_score)
        
        fold += 1
        
    ME = np.mean(me)    
    RMSE = np.mean(rmse)
    ASE = np.mean(ase)
    MSE = np.mean(mse)
    RMSSE = np.mean(rmse)
    
    print("======================================")
    print("Results of", variogram_model)
    print(f'ME overall is {ME:0.6f}')
    print(f'RMSE overall is {RMSE:0.6f}')
    print(f'ASE overall is {ASE:0.6f}')
    print(f'MSE overall is {MSE:0.6f}')
    print(f'RMSSE overall is {RMSSE:0.6f}')
    
def main():
    #define predictor and response variables
    event = General.execute_2()
    cross_validate('spherical', event)
    cross_validate("gaussian", event)
    cross_validate("exponential", event)
    
if __name__ == "__main__":
    main()
