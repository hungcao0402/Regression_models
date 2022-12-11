import sys

sys.path.append(".")

import argparse
import yaml
from sklearn.model_selection import cross_val_score

from utils.dataloader import load_data
from utils.getter import get_instance
from utils.evaluate import MAE_scorer, MAPE_scorer, RMSE_scorer


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path", default="data/Thu-Duc_Weather_Dataset.csv", help="csv data path"
    )
    parser.add_argument(
        "--config_path", default="configs/LinearSGD.yml", help="config file path"
    )
    parser.add_argument("--k_fold", default=5, help="number of k fold")
    parser.add_argument(
        "--weight_path",
        default="weights/LinearSGD.pkl",
        help="weight path to store model",
    )
    parser.add_argument(
        "--val_metric",
        default="MAPE",
        help="validation metric",
    )
    return parser.parse_args()


def train(args):
    # load data
    X_train, y_train, X_test, y_test = load_data(args.data_path)
    # load model
    model_configs = yaml.load(open(args.config_path, "r"), Loader=yaml.Loader)
    model = get_instance(model_configs)
    # train
    model.fit(X_train, y_train)
    # cross validation
    SCORER_DICT = {"MAE": MAE_scorer, "MAPE": MAPE_scorer, "RMSE": RMSE_scorer}
    print(
        f"Cross-validation scores ({args.val_metric} - {args.k_fold} fold(s)) in trainset: ",
        cross_val_score(
            model.model,
            X_train,
            y_train,
            scoring=SCORER_DICT[args.val_metric],
            cv=args.k_fold,
        ),
    )
    # model saving
    print(f"Model was saved in {args.weight_path}")
    model.save_model(args.weight_path)


if __name__ == "__main__":
    args = get_parser()
    train(args)
