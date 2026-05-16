from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATASET_PATH = BASE_DIR / "data" / "raw" / "stream_macroinvertebrates"
OUTPUT_FOLDER = BASE_DIR / "outputs" / "eda"
EDA_OUTPUT_DIR = OUTPUT_FOLDER 
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp")
IMAGE_SIZE = (128, 128)
