import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import DATASET_PATH, OUTPUT_FOLDER
from src.services.eda_service import EDAService
from src.app import MacroApp


def main():
    eda = EDAService(DATASET_PATH, OUTPUT_FOLDER)
    eda.run_all()
    
    # Launch Stage 3 GUI
    app = MacroApp()
    app.mainloop()

if __name__ == "__main__":
    main()
  
