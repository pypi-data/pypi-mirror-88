from typing import Any, Dict

import pandas as pd

from sktmls.autogluon import TabularPrediction as task, __version__


class MLSTrainable:
    def fit(
        self,
        train_data: pd.DataFrame,
        label: str,
        gbm_hyperparameters: Dict[str, Any] = dict(),
        cat_hyperparameters: Dict[str, Any] = dict(),
        eval_metric: str = "roc_auc",
    ) -> None:
        self.model_lib = "autogluon"
        self.model_lib_version = __version__
        self.models[0] = task.fit(
            train_data=train_data,
            label=label,
            presets=["good_quality_faster_inference_only_refit", "optimize_for_deployment"],
            hyperparameters={"GBM": gbm_hyperparameters, "CAT": cat_hyperparameters},
            eval_metric=eval_metric,
            auto_stack=True,
        )

    def evaluate(self, test_data: pd.DataFrame) -> float:
        return self.models[0].evaluate(test_data, silent=True).tolist()

    def feature_importance(self, test_data: pd.DataFrame) -> pd.Series:
        return self.models[0].feature_importance(test_data, silent=True)
