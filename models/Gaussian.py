from Models.Model import Model
from sklearn.gaussian_process import GaussianProcessClassifier as GAUSS_MODEL


class Gaussian(Model):

    def __init__(self):
        super().__init__()

    def create(self):
        self.model = GAUSS_MODEL()
        return self.model


if __name__ == "__main__":
    raise Exception('Impossible to call directly...')
