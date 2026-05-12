from pathlib import Path
import numpy as np 
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""

    def __init__(self, dataframe: pd.DataFrame, output_dir: Path) -> None:
        self.dataframe = dataframe
        self.output_dir = output_dir

    def save_class_distribution(self) -> None:
        """Save a class count chart for the dataset."""
        plt.figure(figsize=(12, 6))
        order = self.dataframe["label"].value_counts().index
        sns.countplot(
        data=self.dataframe,
        x="label",             
        order=order,
        color="#f8e5e5",
        edgecolor="black"
        )
        plt.xticks(rotation=90)
        plt.title("Macroinvertebrate Images per Class")
        plt.xlabel("Class")        
        plt.ylabel("Number of Images")
        plt.tight_layout()
        plt.savefig(self.output_dir / "class_distribution.png")
        plt.close()

    def save_image_size_distribution(self) -> None:
        """Save width and height distribution charts."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.histplot(self.dataframe["width"], bins=20, ax=axes[0], color="#f8e5e5")
        sns.histplot(self.dataframe["height"], bins=20, ax=axes[1], color="#f8e5e5")
        axes[0].set_title("Image Width Distribution")
        axes[1].set_title("Image Height Distribution")
        plt.tight_layout()
        plt.savefig(self.output_dir / "image_size_distribution.png")
        plt.close()

    def build_summary(self) -> dict[str, float]:
        """Return key dataset summary statistics."""
        return {                                        
            "total_images": int(len(self.dataframe)),
            "total_classes": int(self.dataframe["label"].nunique()),
            "mean_width": float(self.dataframe["width"].mean()),
            "mean_height": float(self.dataframe["height"].mean()),
        }                                              

    def save_boxplot(self) -> None:                     
        """Save a box plot of image dimensions per class."""
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        sns.boxplot(
            data=self.dataframe,
            x="label",
            y="width",
            ax=axes[0],
            color="#c39ea0",
        )
        axes[0].set_title("Image Width per Class")
        axes[0].tick_params(axis="x", rotation=90)
        sns.boxplot(
            data=self.dataframe,
            x="label",
            y="height",
            ax=axes[1],
            color="#818D92",
        )
        axes[1].set_title("Image Height per Class")
        axes[1].tick_params(axis="x", rotation=90)

        plt.tight_layout()
        plt.savefig(self.output_dir / "boxplot_dimensions.png")
        plt.close()

    def save_rgb_channels(self) -> None:
        """Compute average RGB channel values and save a bar chart."""
        r_vals, g_vals, b_vals = [], [], []

        for _, row in self.dataframe.iterrows():
            img = cv2.imread(row["file_path"])
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
        plt.savefig(self.output_dir / "rgb_channels.png")
        plt.close()

    def save_brightness_by_class(self) -> None:
        """Save a box plot of mean brightness per class."""
        plt.figure(figsize=(14, 6))
        order = (
            self.dataframe.groupby("label")["brightness"]
            .median()
            .sort_values()
            .index
        )
        sns.boxplot(
            data=self.dataframe,
            x="label",
            y="brightness",
            order=order
        )
        plt.title("Mean Brightness per Class")
        plt.xlabel("Class")
        plt.ylabel("Mean Pixel Brightness (0-255)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(self.output_dir / "brightness_by_class.png")
        plt.close()

    
