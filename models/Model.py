import os

import pandas as pd

from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self):
        self.model = self.create()

    def create(self):
        raise NotImplementedError('You Should implement the Create Method')

    def fit(self, x_data, y_data):
        return self.model.fit(x_data, y_data)

    def predict(self, data):
        return self.model.predict(data)

    def get_accuracy(self, y_data, prediction):
        return accuracy_score(y_data, prediction)

    def get_precision_score(self, y_data, prediction):
        return precision_score(y_data, prediction, average=None)

    def get_recall_score(self, y_data, prediction):
        return recall_score(y_data, prediction, average=None)

    def get_f1_score(self, y_data, prediction):
        return f1_score(y_data, prediction, average=None)

    def get_confusion_matrix(self, y_data, prediction):
        return confusion_matrix(y_data, prediction, normalize='true')

    def separete_train_test_data(self, x_data, y_data, test_size=0.5, stratify=None):
        return train_test_split(x_data, y_data, test_size=0.5, stratify=stratify)

    def run_pre_processor(self, train_x, test_x):
        scaler = StandardScaler()
        scaler.fit(train_x)

        train_x = scaler.transform(train_x)
        test_x = scaler.transform(test_x)

        return train_x, test_x

    def execute(self,
                x_data=None,
                y_data=None,
                filename='results',
                folder	= './results',
				override = True
				):

		self.model = self.create()
		
		raw_train_x, raw_test_x, train_y, test_y = self.separete_train_test_data(x_data, y_data, stratify=y_data)
		train_x, test_x = self.run_pre_processor(raw_train_x, raw_test_x)
		
		self.fit(train_x, train_y)

		predictions = self.predict(test_x)

		data_frame = pd.DataFrame \
            (data=[[self.get_accuracy(test_y, predictions), self.get_precision_score(test_y, predictions),
										self.get_recall_score(test_y, predictions), self.get_f1_score(test_y, predictions),
										self.get_confusion_matrix(test_y, predictions), self.model.classes_, predictions]],
								  columns=['accuracy' ,'precision_score' ,'recall_score' ,'f1_score' ,'confusion_matrix' ,'classes_executed'
                     ,'predictions']
								 )

		self.save_data(data_frame, filename = filename, folder = folder, override = override)

		return data_frame

	def save_data(self, data_frame, filename="model", folder='./results', override=True):

		if not os.path.exists(folder):
			os.makedirs(folder)

		if override:
			data_frame.to_csv(f'{folder}/{filename}', mode='w', index=False, sep=';')
		else:
			if os.path.exists(f'{folder}/{filename}'):
				data_frame.to_csv(f'{folder}/{filename}', mode='a', index=False, sep=';', header=None)
			else:
				data_frame.to_csv(f'{folder}/{filename}', mode='a', index=False, sep=';')

if __name__ == "__main__":
	raise Exception('Impossible to call directly...')
