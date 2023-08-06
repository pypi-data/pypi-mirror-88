from typing import Dict, NewType, Union

import numpy as np
import pandas as pd


ModelObject = NewType("ModelObject", object)

try:
    import pyspark.sql.dataframe

    MlModelInferableDataset = Union[
        pd.DataFrame, np.ndarray, Dict[str, np.ndarray], pyspark.sql.dataframe.DataFrame
    ]
except ImportError:
    MlModelInferableDataset = Union[pd.DataFrame, np.ndarray, Dict[str, np.ndarray]]
