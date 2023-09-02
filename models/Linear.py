from Models.Model import Model
from sklearn.svm import LinearSVC as LINEAR_MODEL


class Linear(Model):

    def __init__(self):
        super().__init__()

    def create(self):
        self.model = LINEAR_MODEL()
        return self.model


if __name__ == "__main__":
    raise Exception('Impossible to call directly...')
