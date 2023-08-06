import importlib
import numpy as np
import pandas as pd
import os
import sys
import tensorflow as tf
from sklearn.utils import shuffle
from importlib import import_module
import pickle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config = importlib.import_module('config')

import configparser

class Utils:
    def __init__(self):
        cg = configparser.ConfigParser()
        cg.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'initial.ini'),
                encoding='utf-8')
        self.cur_task_path = cg.get('task','cur_task_path')

        if self.cur_task_path != 'None':
            self.__get_data(self.cur_task_path)


    def __get_data(self,task_path):
        cg = configparser.ConfigParser()
        cg.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'initial.ini'), encoding='utf-8')
        cg.set('task', 'cur_task_path', task_path)


        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'initial.ini'), 'w', encoding='utf-8') as f:
            cg.write(f)

        file_name_list = os.listdir(task_path)
        data_path = None

        for file_name in file_name_list:
            if 'dataset' in file_name:
                data_path = os.path.join(task_path, file_name)

        if not data_path:
            print('没有发现病案文件，请确保为*.xlsx格式并在当前目录下！')



        data = pd.read_excel(data_path,header=0)
        data.dropna(axis=0,how='any',inplace=True)
        data = data.reset_index(drop=True)
        data = shuffle(data,random_state=config.config.random_num)


        x_name = data.columns.values

        self.x_name = list(x_name)[:-1]
        self.x_num = len(self.x_name)

        self.data = np.array(data)

        self.cla_name = list(set(self.data[:,-1]))
        self.cla_num = len(self.cla_name)

        self.cur_data = self.data  # 在生成权重时候，会以此数据为基准。 仅在交叉验证时，这个值会被动态赋值成训练集。其他时候都为全数据集

    def __get_fre_x2c(self, x_id, cla_name):
        data = self.cur_data[self.cur_data[:, -1] == cla_name][:, :-1]
        frq_x2c = data[:, x_id].sum()
        return frq_x2c

        # 获取在所有样本中，指定x的频次

    def __get_frq_x2C(self, x_id):
        data = self.cur_data[:, :-1]
        frq_x2C = data[:, x_id].sum()
        return frq_x2C

        # 获取在指定分类下，所有X的平均频次

    def __get_frq_X2c(self, cla_name):
        data = pd.DataFrame(self.cur_data[self.cur_data[:, -1] == cla_name][:, :-1])
        frq_X2c = 0
        for i in range(data.shape[1]):
            frq_X2c += np.array(data)[:, i].sum()
        return frq_X2c

        # 获取在所有样本里，所有X的平均频次

    def __get_frq_X2C(self):
        data = pd.DataFrame(self.cur_data[:, :-1])
        frq_X2C = 0
        for i in range(data.shape[1]):
            frq_X2C += np.array(data)[:, i].sum()
        return frq_X2C

    def __get_x2c(self, x_id, cla_name):
        x2c = self.__get_fre_x2c(x_id, cla_name)
        w_c = self.cur_data[self.cur_data[:, -1] == cla_name][:, :-1].shape[0]
        h_c = w_c / 2

        return (x2c - h_c) / w_c

    def __get_x2C(self, x_id):
        x2C = self.__get_frq_x2C(x_id)
        w_C = self.cur_data[:, :-1].shape[0]
        h_C = w_C / 2
        return (x2C - h_C) / w_C

    def __get_X2c(self, cla_name):
        X2c = self.__get_frq_X2c(cla_name)
        w_c = self.cur_data[self.cur_data[:, -1] == cla_name][:, :-1].shape[0] * \
              self.cur_data[self.cur_data[:, -1] == cla_name][:, :-1].shape[1]
        h_c = w_c / 2
        return (X2c - h_c) / w_c

    def __get_X2C(self):
        X2C = self.__get_frq_X2C()
        w_C = self.cur_data[:, :-1].shape[0] * self.cur_data[:, :-1].shape[1]
        h_C = w_C / 2
        return (X2C - h_C) / w_C

    def __get_x2all(self,x_id,):
        x2all_list = []
        x2all_list_debug = []
        obtained_X2C = self.__get_X2C()
        obtained_x2C = self.__get_x2C(x_id)
        for i in range(self.cla_num):

            cla_name = self.cla_name[i]
            obtained_X2c = self.__get_X2c(cla_name)

            x2all_list.append(   (
                            (self.__get_x2c(x_id,cla_name) - obtained_x2C) * (1+abs(obtained_X2C-0.5))
                              +
                              (obtained_X2c - obtained_X2C)

                                )
                            )


            x2all_list_debug.append('{},{},{},{}'.format(
                self.__get_x2c(x_id,cla_name),
                obtained_x2C,
                obtained_X2c,
                obtained_X2C
                )

            )

        return x2all_list, x2all_list_debug

    def __get_all2all(self):


        weigh = pd.DataFrame(np.zeros(shape=(self.x_num, self.cla_num)),columns=self.cla_name,index=self.x_name)
        weigh_debug = pd.DataFrame(np.zeros(shape=(self.x_num, self.cla_num)),columns=self.cla_name,index=self.x_name)

        for x_id in range(self.x_num):
            x2all_list, x2all_list_debug = self.__get_x2all(x_id)

            weigh.iloc[x_id, :] = np.array(x2all_list)
            weigh_debug.iloc[x_id, :] = np.array(x2all_list_debug)

        return weigh, weigh_debug

    def get_weigh_corr(self,task_path,force_refresh=False):


        x,y = self.get_xy_onehot(task_path)

        save_path = os.path.join(os.path.join(task_path,'weigh') ,'{}_weigh.ckpt'.format('SANN'))
        weigh_path = os.path.join(task_path, '{}_weigh.xlsx'.format('SANN'))
        corr_path = os.path.join(task_path, '{}_corr.xlsx'.format('SANN'))

        if os.path.exists(weigh_path) and not force_refresh:
            if os.stat(weigh_path).st_size > 0:
                print('{}-{}权值及相关系数已存在，跳过......'.format('SANN',os.path.basename(task_path)))
                return None


        cur_weigh, debug_weigh = self.__get_all2all()
        corr = self.get_corr(cur_weigh)

        model_file = import_module('model.{}'.format('SANN'))
        model = model_file.Model(trainable=True, initial_weigh=[corr, cur_weigh])


        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[tf.keras.metrics.CategoricalAccuracy()
                                                                                  ])
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(filepath=save_path, save_best_only=True,save_weights_only=True),
            tf.keras.callbacks.EarlyStopping(patience=config.config.patience_num, min_delta=1e-3)
        ]

        history = model.fit(
            x=x,
            y=y,
            validation_split=0.2,
            batch_size=config.config.batch_size,
            epochs=config.config.epochs_num,
            callbacks=callbacks)

        model.load_weights(save_path)


        pd.DataFrame(model.get_weights()[1],
                 columns=self.cla_name,
                 index=self.x_name).to_excel(weigh_path)

        pd.DataFrame(model.get_weights()[0],
                 columns=self.x_name,
                 index=self.x_name).to_excel(corr_path)

        print('{}-{}权值及相关系数生成完毕'.format('SANN', os.path.basename(task_path)))

    def get_corr(self,cur_weigh,force_refresh=False):

        # # 皮尔逊相关系数
        # data = pd.DataFrame(self.cur_data[:, :-1],
        #                     columns=self.x_name)
        # corr = data.corr()
        #
        # corr.fillna(0, inplace = True)

        # 利用对分类的贡献度的相似性生成相关系数
        data = pd.DataFrame(cur_weigh,
                            index=self.x_name,
                            columns=self.cla_name)
        corr = pd.DataFrame(np.zeros(shape=[self.x_num,self.x_num]),
                            index=self.x_name,
                            columns=self.x_name)

        for cla_name in self.cla_name:
            cur_data = np.array(data.loc[:,cla_name])
            for x_id in range(self.x_num):

                x_x_cla_temp = []

                x_value = cur_data[x_id]
                max_difference_v = max(abs(x_value-np.max(cur_data)),abs(x_value-np.min(cur_data)))

                for x_id_again in range(self.x_num):
                    difference_value = abs(cur_data[x_id] - cur_data[x_id_again])

                    # 判断是否同号
                    if max(cur_data[x_id],0) == max(cur_data[x_id_again],0):

                        corr_value = 1- (difference_value/max_difference_v)

                    else:
                        corr_value = - (difference_value/max_difference_v)

                    x_x_cla_temp.append(corr_value)

                corr.iloc[x_id,:] += x_x_cla_temp

        corr /= self.cla_num

        return np.array(corr)

    def get_xy_cross_val(self,task_path,k,force_refresh=False):

        save_path = os.path.join(task_path,'cross_val_data.pkl')



        self.__get_data(task_path)

        xy_cross_val_list = []

        if os.path.exists(save_path) and not force_refresh:
            with open(save_path,'rb') as f:
                xy_cross_val_list = pickle.load(f)
            return xy_cross_val_list


        def get_xy_split(test_index):

            x = self.data[:, :-1]
            y = tf.keras.utils.to_categorical(self.data[:, -1]-1)

            train_x = np.delete(x,test_index,axis=0)
            test_x = x[test_index,:]

            train_y = np.delete(y,test_index,axis=0)
            test_y = y[test_index,:]

            self.cur_data = np.delete(self.data,test_index,axis=0)
            weigh,weigh_Debug = self.__get_all2all()
            corr = self.get_corr(weigh)

            return [train_x, train_y, test_x, test_y, [corr,np.array(weigh)]]


        k_len = self.data.shape[0]//k
        start = 0
        while True:

            end = start + k_len
            if self.data.shape[0] - end < k_len:
                end = self.data.shape[0]

            test_index  = [i for i in range(start,end)]
            xy_cross_val_list.append(get_xy_split(test_index))
            start = end

            if end == self.data.shape[0]:
                break

        self.cur_data = self.data

        with open(save_path, 'wb') as f:
            pickle.dump(xy_cross_val_list,f)
        return xy_cross_val_list

    def get_xy_onehot(self,task_path):
        self.__get_data(task_path)
        x = self.data[:, :-1]
        y = tf.keras.utils.to_categorical(self.data[:, -1] - 1)

        return x,y

    def get_xy(self,task_path):
        self.__get_data(task_path)
        x = self.data[:, :-1]
        y = self.data[:, -1]

        return x,y

    def onhot2id(self,y_onehot):
        y_ori_list = np.argmax(y_onehot,axis=1)
        y_id = [y_ori+1 for y_ori in y_ori_list]
        return np.array(y_id)

    def get_xy_onehot_classes(self,task_path,):

        self.__get_data(task_path)

        xy_classes = []

        columns = self.x_name.copy()
        columns.append('cla')
        data = pd.DataFrame(self.data.copy(),columns=columns)

        for i in set(data.iloc[:, -1]):
            x = data.loc[data['cla']==i].iloc[:,:-1]
            y = tf.keras.utils.to_categorical(data.loc[data['cla']==i].iloc[:,-1] - 1,num_classes=len(set(data.iloc[:, -1])))

            xy_classes.append((i,x,y))

        return xy_classes

utils = Utils()

if __name__ == '__main__':
    pass

