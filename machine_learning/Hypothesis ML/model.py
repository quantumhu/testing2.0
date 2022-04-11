import os
import joblib
import pandas as pd
from ml_base import MLModel
from __init__ import __version__
from schema import TitanicModelInput, TitanicModelOutput




class TitanicModel(MLModel):
    """Prediction functionality of the Titanic Model."""

    @property
    def display_name(self) -> str:
        """Return display name of model."""
        return "Titanic Model"

    @property
    def qualified_name(self) -> str:
        """Return qualified name of model."""
        return "titanic_model"

    @property
    def description(self) -> str:
        """Return description of model."""
        return "Model to predict the survival of titanic passengers."

    @property
    def version(self) -> str:
        """Return version of model."""
        return __version__

    @property
    def input_schema(self):
        """Return input schema of model."""
        return TitanicModelInput

    @property
    def output_schema(self):
        """Return output schema of model."""
        return TitanicModelOutput

    def __init__(self):
        """Class constructor that loads and deserializes the model parameters.
        .. note::
            The trained model parameters are loaded from the "model_files" directory.
        """
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        with open(os.path.join(dir_path,"CISC 499", "model.joblib"), 'rb') as file:
            self._rf_model = joblib.load(file)

    def predict(self, data: TitanicModelInput) -> TitanicModelOutput:
        """Make a prediction with the model.
        :param data: Data for making a prediction with the model. Object must meet requirements of the input schema.
        :rtype: The result of the prediction, the output object will meet the requirements of the output schema.
        """
        # converting the incoming data into a pandas dataframe that can be accepted by the model
        X = pd.DataFrame([[data.Age, data.Sex, data.Pclass, data.SibSp,
                           data.Parch, data.Fare, data.Embarked]],
                         columns=["Age", "Sex", "Pclass", "SibSp",
                                  "Parch", "Fare", "Embarked"])

        # making the prediction and extracting the result from the array
        y_hat = self._rf_model.predict(X)[0]

        return TitanicModelOutput(Survived=y_hat)