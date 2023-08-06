import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from sktmls.autogluon import TabularPrediction as task, __version__

MLS_MODEL_DIR = Path.home().joinpath("models")


class MLSTrainable:
    def fit(
        self,
        train_data: pd.DataFrame,
        label: str,
        test_data: pd.DataFrame = None,
        gbm_hyperparameters: Dict[str, Any] = dict(),
        cat_hyperparameters: Dict[str, Any] = dict(),
        eval_metric: str = "roc_auc",
    ) -> None:

        self.model_lib = "autogluon"
        self.model_lib_version = __version__
        self.metric = eval_metric

        model_binary = task.fit(
            train_data=train_data,
            label=label,
            presets=["good_quality_faster_inference_only_refit"],
            hyperparameters={"GBM": gbm_hyperparameters, "CAT": cat_hyperparameters},
            eval_metric=eval_metric,
            auto_stack=True,
            output_directory=MLS_MODEL_DIR.joinpath(self.model_name, self.model_version),
        )

        model_binary.delete_models(models_to_keep="best", dry_run=False)
        model_binary.save_space(remove_data=True, remove_fit_stack=False, requires_save=False, reduce_children=False)

        self.models[0] = model_binary

        if test_data is not None:
            self.performance = self.evaluate(test_data)
            self.feature_importance = json.dumps(self.feature_importance(test_data).to_dict())

    def evaluate(self, test_data: pd.DataFrame) -> float:
        return self.models[0].evaluate(test_data, silent=True).tolist()

    def feature_importance(self, test_data: pd.DataFrame) -> pd.Series:
        return self.models[0].feature_importance(test_data, silent=True)

    def set_mms_path(self) -> None:
        trainer = self.models[0]._learner.load_trainer()
        for model_name in trainer.get_model_names_all():
            trainer.set_model_attribute(
                model_name, "path", f"/models/{self.model_name}/{self.model_version}/models/{model_name}/"
            )

    def set_local_path(self) -> None:
        trainer = self.models[0]._learner.load_trainer()
        for model_name in trainer.get_model_names_all():
            trainer.set_model_attribute(
                model_name, "path", f"{MLS_MODEL_DIR}/{self.model_name}/{self.model_version}/models/{model_name}/"
            )
