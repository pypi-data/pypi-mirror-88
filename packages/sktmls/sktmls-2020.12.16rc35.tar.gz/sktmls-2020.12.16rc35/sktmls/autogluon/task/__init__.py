import logging

logging.basicConfig(format="%(message)s")  # just print message in logs

from .base import BaseTask
from .tabular_prediction import TabularPrediction
