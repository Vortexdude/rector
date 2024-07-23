import os
from app.core.config import settings
from app.common.utils.files import upload_file
from .processing import create_image


class RectorImageService:
    def __init__(self, model, input_file) -> None:
        self.model = model
        self.input_file = input_file
        self.model_path = None
        self.model_base_path = None
        self.input_image_path = None
        self.output_image_path = None

    def _join_paths(self) -> None:
        self.model_base_path = settings.NURAL_NETWORK_STYLE_PATH
        self.input_image_path = os.path.join(settings.UPLOAD_DIR, self.input_file.filename)
        self.output_image_path = os.path.join(settings.OUTPUT_DIR, f"{self.model}_{self.input_file.filename}")

    def process(self) -> str:
        model_filename = f"{self.model.replace('-', '/')}.t7" if "-" in self.model else f"{self.model}.t7"
        upload_file(self.input_file, settings.UPLOAD_DIR)
        self._join_paths()
        self.model_path = os.path.join(self.model_base_path, model_filename)
        create_image(self.model_path, self.input_image_path, self.output_image_path)
        return self.output_image_path
