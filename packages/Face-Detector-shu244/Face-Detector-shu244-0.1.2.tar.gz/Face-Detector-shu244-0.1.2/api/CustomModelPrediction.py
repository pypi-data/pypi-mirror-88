import os
import numpy as np

class CustomModelPrediction(object):
    def __init__(self, model):
        # Stores artifacts for prediction. Only initialized via `from_path`.
        self._model = model

    def predict(self, instances, **kwargs):
        """
        Performs custom prediction.

        Instances are the decoded values from the request. They have already
        been deserialized from JSON.

        Args:
            instances: A list of prediction input instances.
            **kwargs: A dictionary of keyword args provided as additional
                fields on the predict request body.

        Returns:
            A list of outputs containing the prediction results. This list must
            be JSON serializable.
        """

        # results = []
        # for image in instances:
        #     image = np.asarray(image)
        #     result = self._model(image)
        #     results.append(result)
        # return results
        return 'Test results'

    @classmethod
    def from_path(cls, model_dir):
        """
        Creates an instance of CustomModelPrediction using the given path.

        This loads artifacts that have been copied from your model directory in
        Cloud Storage. CustomModelPrediction uses them during prediction.

        Args:
            model_dir

        Returns:
            An instance of `MyPredictor`.
        """

        from face_detector.interface import FaceDetectorInterface

        model_param_path = os.path.join(model_dir, 'yolov3_ckpt_2.pth')
        model_arch_path = os.path.join(model_dir, 'yolov3-custom.cfg')
        class_names_path = os.path.join(model_dir, 'classes.names')
        interface = FaceDetectorInterface.create(model_param_path, model_arch_path, class_names_path)

        return cls(interface)


