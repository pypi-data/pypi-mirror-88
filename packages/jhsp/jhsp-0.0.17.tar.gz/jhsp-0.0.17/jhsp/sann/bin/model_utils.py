import importlib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from os import path,stat
import time
import pickle
import numpy as np
from importlib import import_module
import tensorflow as tf
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config = importlib.import_module('config')
data_utils = importlib.import_module('data_utils')
other_utils = importlib.import_module('other_utils')

class Utils:
    def __init__(self):
        RF_parameters = {
            'n_estimators': range(20, 800, 10),
            'criterion': ['entropy', 'gini'],
            'max_depth': range(5, 25, 1),
            'max_features': ['auto', 'sqrt', 'log2'],
            'min_samples_split': range(2, 5, 1),
        }

        KNN_parameters = {
            'n_neighbors': range(1, 10, 1),
            'weights': ['uniform', 'distance'],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
        }

        SVC_parameters = {
            'C': np.arange(1, 8, 0.2),
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'gamma': ['scale', 'auto'],
            'degree': range(1, 11, 1)
        }

        self.param_dict = {'RF': RF_parameters,
                      'KNN': KNN_parameters,
                      'SVC': SVC_parameters}
        self.model_name_list = ['RF','KNN','SVC']

        self.cla_dict ={'RF':RandomForestClassifier(),
                           'KNN':KNeighborsClassifier(),
                           'SVC':SVC()}

    def __get_model_best(self,model_name,task_path,force_refresh):

            save_path = path.join(task_path, '{}_ini.pkl'.format(model_name))

            print('最优化模型{},{}......'.format(model_name,path.basename(task_path)))
            start = time.time()

            if path.exists(save_path) and not force_refresh:
                if stat(save_path).st_size > 0:
                    print('最优化模型已存在，跳过......')
                    return None

            x,y = data_utils.utils.get_xy(task_path)


            random_search = RandomizedSearchCV(self.cla_dict[model_name],
                                               param_distributions=self.param_dict[model_name],
                                               n_iter=config.config.random_search_n_iter,
                                               cv=config.config.cross_val_num,
                                               scoring='accuracy',
                                               random_state = config.config.random_num
                                               # n_jobs= -1
                                               )

            random_search.fit(x,y)

            best_params = random_search.cv_results_['params'][random_search.best_index_]

            with open(save_path,'wb') as f:
                pickle.dump(best_params,f)

            end = time.time()
            print('优化完成，耗时:{}'.format(end-start))

    def get_all_model_best(self,task_path,force_refresh=False):
        for model_name in self.model_name_list:
            self.__get_model_best(model_name,task_path,force_refresh)

    def get_model(self,model_name,task_path,initial_weigh=None):

        if model_name not in ['SANN','ANN']:
            with open(path.join(task_path, model_name + '_ini.pkl'),'rb') as f:
                ini_dict = pickle.load(f)
        else:
            x, y = data_utils.utils.get_xy_onehot(task_path)

        if model_name == 'RF':
            model = RandomForestClassifier(n_estimators=ini_dict['n_estimators'],
                                           criterion=ini_dict['criterion'],
                                           max_depth=ini_dict['max_depth'],
                                           max_features=ini_dict['max_features'],
                                           min_samples_split=ini_dict['min_samples_split'],
                                           random_state = config.config.random_num
                                           )

        elif model_name == 'KNN':
            model = KNeighborsClassifier(n_neighbors=ini_dict['n_neighbors'],
                                         weights=ini_dict['weights'],
                                         algorithm=ini_dict['algorithm']
                                         )

        elif model_name == 'SVC':
            model =SVC(
                C=ini_dict['C'],
                kernel=ini_dict['kernel'],
                gamma=ini_dict['gamma'],
                degree=ini_dict['degree'],
                random_state = config.config.random_num)


        elif model_name in ['SANN','ANN']:

            model_file = import_module('model.{}'.format(model_name))
            model = model_file.Model(trainable=True, initial_weigh=initial_weigh)



        return model



utils = Utils()

if __name__ == '__main__':
    pass