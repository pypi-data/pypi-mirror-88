import os
import configparser




class Config:
    def __init__(self):

        cg = configparser.ConfigParser()
        cg.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'initial.ini'), encoding='utf-8')


        self.input_path = cg.get('path','input_path')


        task_name_list_str = cg.get('task', 'task_name_list').strip(',')
        self.task_name_list = task_name_list_str.split(',')


        self.task_path_list = [os.path.join(self.input_path,task_name) for task_name in self.task_name_list]
        self.model_path = 'model.simple_net'
        self.cross_val_num = 5
        self.epochs_num = 1500
        self.drop_rate = 0
        self.random_search_n_iter = 100
        self.random_search_n_jobs = -1
        self.batch_size = 300
        self.model_list = ['SANN','ANN','KNN','SVC','RF']
        self.metrics_list = ['accuracy','precision','recall','f1']
        self.random_num = 100
        self.legend_loc = 3
        self.patience_num = 100

config = Config()

if __name__ == '__main__':
    pass