from sklearn.linear_model import LogisticRegression
from models import GrapeModule
from dataprocessing import load_data
from training import (
    train_grape, 
    train_logistic_regression,
    eval_grape,
    eval_logistic_regression
)

from dataclasses import dataclass

from typing import Dict, Any, Callable


@dataclass
class ModelConfig:
    name: str
    model: Callable
    train_procedure: Callable
    eval_procedure: Callable
    model_kwargs: Dict


@dataclass
class ExperimentConfig:
    models: Dict[str, ModelConfig]


def train_model(config: ModelConfig, X, y):
    model = config.model(**config.model_kwargs)
    model, train_loss = config.train_procedure(model, X, y)
    print(f"Trained model {config.name} - train loss: {train_loss}")
    return model


def run_experiment(config: ExperimentConfig):
    X_train, y_train, X_test, y_test = load_data()

    metrics = dict()
    for name, model in config.models.items():
        trained_model = train_model(model, X_train, y_train)
        metrics[model.name] = model.eval_procedure(trained_model, X_test, y_test)

    return metrics


if __name__=="__main__":
    config = ExperimentConfig(
        models = {
            'logistic_regression': ModelConfig(
                name='LogisticRegression',
                model=LogisticRegression,
                train_procedure=train_logistic_regression,
                eval_procedure=eval_logistic_regression,
                model_kwargs=dict(),
            ),
            'grape': ModelConfig(
                name='GRAPE',
                model=GrapeModule,
                train_procedure=train_grape,
                eval_procedure=eval_grape,
                model_kwargs={
                    'emb_dim': 4,
                    'n_layers': 2,
                    'edge_dim': 1,
                    'out_dim': 19,
                    'n_genes': 3451,
                },
            )
        }

    )
    print(run_experiment(config))
