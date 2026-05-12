import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import DATASET_PATH, OUTPUT_FOLDER
from src.services.eda_service import EDAService
def main():
    eda = EDAService(DATASET_PATH, OUTPUT_FOLDER)
    eda.run_all()

if __name__ == "__main__":
    main()
