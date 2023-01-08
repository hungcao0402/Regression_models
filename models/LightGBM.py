from models.base_model import BaseModel
import pickle as pkl
import lightgbm as lgb

class LightGBM(BaseModel):
    def __init__(self, opt):
        self.model = lgb.LGBMRegressor(**opt)
        # self.model = lgb.LGBMRegressor()
    def fit(self, X, y):
        self.model.fit(X, y)

    def save_model(self, weight_path):
        pkl.dump(self.model, open(weight_path, "wb"))

    def load_model(self, weight_path):
        self.model = pkl.load(open(weight_path, "rb"))

    def predict(self, X):
        return self.model.predict(X)
