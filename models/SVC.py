from Models.Model import Model
from sklearn.svm import SVC as SVC_MODEL


class SVC(Model):

    def __init__(self):
        super().__init__()

    def create(self):
        self.model = SVC_MODEL()
        return self.model


if __name__ == "__main__":
    raise Exception('Impossible to call directly...')
