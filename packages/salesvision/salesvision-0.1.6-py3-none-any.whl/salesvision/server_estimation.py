import io
import requests
from PIL import Image

from salesvision.image_utils import read_image


class EstimationTemplate(object):
    def __call__(self, image_object) -> dict:
        raise NotImplementedError()


class ServerEstimator(EstimationTemplate):
    def __init__(self,
                 server_ip: str = '87.117.25.190',
                 server_port: int = 5015):
        """
        Class constructor
        Args:
            server_ip: estimation server id address in format *.*.*.*
            server_port: estimation server port
        """
        self.address = 'http://{}:{}'.format(server_ip, server_port)

        response = requests.get(
            url='{}/api/test/ping/'.format(self.address)
        )

        if response.status_code != 200:
            raise RuntimeError(
                'Can\'t connect to server: {}'.format(self.address)
            )

    def _analyze_image(self, image: Image):
        """
        Server inference on image
        Args:
            image: image in Pillow format

        Returns:
            Dict with prediction
        """
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='JPEG')
        img_byte_array = img_byte_array.getvalue()

        response = requests.post(
            url='{}/api/inference/client_fashion_analysis/'.format(
                self.address
            ),
            files={"file": ("filename", img_byte_array, "image/jpeg")}
        )

        if response.status_code != 200:
            raise RuntimeError(
                'Request fail with code: {}'.format(response.status_code)
            )

        results = response.json()

        return results

    def __call__(self, image_object) -> dict:
        """
        Insert image description to database
        Args:
            image_object: image path on local machine or URL link or Array

        Returns:
            Prediction in dictionary format
        """
        image = read_image(image_object)

        return self._analyze_image(image)
