#config
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATASET_PATH = BASE_DIR / "data" / "raw" / "stream_macroinvertebrates"
OUTPUT_FOLDER = BASE_DIR / "outputs" / "eda"

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp")
IMAGE_SIZE = (128, 128)

#main
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import DATASET_PATH, OUTPUT_FOLDER
from src.services.eda_service import EDAService

def main():
    eda = EDAService(DATASET_PATH, OUTPUT_FOLDER)
    eda.run_all()

if __name__ == "__main__":
    main()

#eda_service
import os
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns


class EDAService:
    """Generate and save EDA outputs for the macroinvertebrate image dataset."""

    def __init__(self, dataset_path, output_folder) -> None:
        self.dataset_path = dataset_path
        self.output_folder = output_folder
        self.df = None

    def build_dataframe(self) -> pd.DataFrame:
        """Scan dataset folder and build a DataFrame with image metadata."""
        data = []
        for label in os.listdir(self.dataset_path):
            folder = os.path.join(self.dataset_path, label)
            if not os.path.isdir(folder):
                continue

            for fname in os.listdir(folder):
                if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                    continue

                img_path = os.path.join(folder, fname)
                img = cv2.imread(img_path)
                if img is None:
                    continue

                h, w = img.shape[:2]
                channels = img.shape[2] if len(img.shape) == 3 else 1

                # NumPy: compute mean brightness across all channels
                brightness = float(np.mean(img))

                data.append({
                    "path": img_path,
                    "label": label,
                    "width": w,
                    "height": h,
                    "channels": channels,
                    "brightness": round(brightness, 2),
                })

        self.df = pd.DataFrame(data)
        return self.df

    def print_summary(self) -> dict:
        """Print and return key dataset summary statistics."""
        summary = {
            "total_images": int(len(self.df)),
            "total_classes": int(self.df["label"].nunique()),
            "mean_width": float(self.df["width"].mean()),
            "mean_height": float(self.df["height"].mean()),
            "mean_brightness": float(self.df["brightness"].mean()),
        }
        print("===== STAGE 1 EDA SUMMARY =====")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        print("\nPreview:")
        print(self.df.head())
        return summary

    def save_class_distribution(self) -> None:
        """Save a bar chart showing number of images per class."""
        plt.figure(figsize=(12, 5))
        order = self.df["label"].value_counts().index
        sns.countplot(data=self.df, x="label", order=order)
        plt.title("Macroinvertebrate Images per Class")
        plt.xlabel("Class")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(self.output_folder / "class_distribution.png")
        plt.close()
        print("  Saved: class_distribution.png")

    def save_size_plots(self) -> None:
        """Save width and height distribution histograms side by side."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.histplot(self.df["width"], bins=20, ax=axes[0], color="lightgreen")
        sns.histplot(self.df["height"], bins=20, ax=axes[1], color="salmon")
        axes[0].set_title("Image Width Distribution")
        axes[1].set_title("Image Height Distribution")
        plt.tight_layout()
        plt.savefig(self.output_folder / "image_size_distribution.png")
        plt.close()
        print("  Saved: image_size_distribution.png")

    def save_boxplot(self) -> None:
        """Save a box plot comparing width and height spread."""
        plt.figure(figsize=(10, 5))
        sns.boxplot(data=self.df[["width", "height"]])
        plt.title("Width & Height Box Plot")
        plt.ylabel("Pixels")
        plt.tight_layout()
        plt.savefig(self.output_folder / "size_boxplot.png")
        plt.close()
        print("  Saved: size_boxplot.png")

    def save_rgb_channels(self) -> None:
        """Compute average RGB channel values using NumPy and save a bar chart."""
        r_vals, g_vals, b_vals = [], [], []

        for _, row in self.df.iterrows():
            img = cv2.imread(row["path"])
            if img is None:
                continue
            b_vals.append(np.mean(img[:, :, 0]))
            g_vals.append(np.mean(img[:, :, 1]))
            r_vals.append(np.mean(img[:, :, 2]))

        plt.figure(figsize=(6, 4))
        plt.bar(
            ["Red", "Green", "Blue"],
            [np.mean(r_vals), np.mean(g_vals), np.mean(b_vals)],
            color=["red", "green", "blue"],
        )
        plt.title("Average RGB Channel Values Across Dataset")
        plt.ylabel("Mean Pixel Value (0-255)")
        plt.tight_layout()
        plt.savefig(self.output_folder / "rgb_channels.png")
        plt.close()
        print("  Saved: rgb_channels.png")

    def save_brightness_by_class(self) -> None:
        """Save a box plot of mean brightness per class."""
        plt.figure(figsize=(14, 6))
        order = (
            self.df.groupby("label")["brightness"]
            .median()
            .sort_values()
            .index
        )
        sns.boxplot(data=self.df, x="label", y="brightness", order=order)
        plt.title("Mean Brightness per Class")
        plt.xlabel("Class")
        plt.ylabel("Mean Pixel Brightness (0-255)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(self.output_folder / "brightness_by_class.png")
        plt.close()
        print("  Saved: brightness_by_class.png")

    def save_sample_grid(self) -> None:
        """Save a 3x3 grid of random sample images for visual inspection."""
        sample_df = self.df.sample(min(9, len(self.df)), random_state=42)

        fig, axes = plt.subplots(3, 3, figsize=(10, 10))
        for ax, (_, row) in zip(axes.flat, sample_df.iterrows()):
            img = cv2.imread(row["path"])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img)
            ax.set_title(row["label"], fontsize=8)
            ax.axis("off")

        for ax in axes.flat[len(sample_df):]:
            ax.axis("off")

        plt.tight_layout()
        plt.savefig(self.output_folder / "sample_images.png")
        plt.close()
        print("  Saved: sample_images.png")

    def save_plotly_chart(self) -> None:
        """Save an interactive Plotly HTML chart of class distribution."""
        fig = px.histogram(
            self.df,
            x="label",
            title="Class Count (Interactive)",
            labels={"label": "Class", "count": "Count"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig.write_html(str(self.output_folder / "plotly_classes.html"))
        print("  Saved: plotly_classes.html")

    def run_all(self) -> None:
        """Run all EDA steps in sequence."""
        os.makedirs(self.output_folder, exist_ok=True)
        print("\n===== Running Stage 1 EDA =====")
        self.build_dataframe()
        print(f"DEBUG: DataFrame shape = {self.df.shape}") 
        print(f"DEBUG: Columns = {self.df.columns.tolist()}")
        self.print_summary()
        print("\nGenerating charts...")
        self.save_class_distribution()
        self.save_size_plots()
        self.save_boxplot()
        self.save_rgb_channels()
        self.save_brightness_by_class()
        self.save_sample_grid()
        self.save_plotly_chart()
        print(f"\nAll EDA outputs saved to: {self.output_folder}")

#records
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ImageRecord:
    """Store the core metadata for one indexed macroinvertebrate image."""

    file_path: Path
    label: str
    width: int
    height: int
    channels: int
