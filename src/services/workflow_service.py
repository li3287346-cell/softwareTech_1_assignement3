import pandas as pd
from src.config import EDA_OUTPUT_DIR
from src.services.dataset_indexer import DatasetIndexer
from src.services.eda_service import EDAService



class WorkflowService:
    """Coordinate the Stage 1 EDA workflow."""

    def __init__(self) -> None:
        EDA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.indexer = DatasetIndexer()
        self.dataframe: pd.DataFrame | None = None

    def load_dataframe(self) -> pd.DataFrame:
        """Load and cache the indexed dataset."""
        if self.dataframe is None:
            self.dataframe = self.indexer.build_dataframe()
        return self.dataframe

    def show_summary(self) -> dict[str, float]:
        """Build and print dataset summary statistics."""
        dataframe = self.load_dataframe()
        eda = EDAService(dataframe, EDA_OUTPUT_DIR)
        summary = eda.build_summary()
        print(summary)
        return summary

    def run_full_pipeline(self) -> None:
        """Run the full Stage 1 workflow."""
        print("Running EDA...")
        self.show_summary()
        self.generate_eda()
        print("EDA complete! Check outputs/eda/")

    def generate_eda(self) -> None:
        """Create and save the main EDA outputs."""
        dataframe = self.load_dataframe()
        eda = EDAService(dataframe, EDA_OUTPUT_DIR)
        eda.save_class_distribution()
        eda.save_image_size_distribution()
        eda.save_boxplot()
        eda.save_rgb_channels()
        eda.save_brightness_by_class()
        eda.save_sample_grid()
