# softwareTech_1_assignement3
## Project Goal
This project builds a modular Python application that analyses a macroinvertebrate image dataset sourced from Kaggle. The system scans and indexes images into a structured table, performs exploratory data analysis to examine class distributions, image dimensions, colour properties and brightness levels, and displays the results through an interactive Tkinter desktop application.
## Main Features
Automatic dataset indexing from folder structure
Six EDA chart outputs:
Class distribution bar chart
Image size distribution histogram
Sample image grid
Box plot of image dimensions per class
RGB channel analysis
Brightness by class analysis

Interactive desktop GUI built with Tkinter
Sidebar navigation to browse between charts
Button highlight showing currently selected chart
Dataset summary panel showing key statistics
Export any chart to a chosen location with one click

## How to Run
1. Install dependencies with `pip install -r requirements.txt`
2. Place the dataset inside `data/raw`
3. Run `python -m src.main` for the full pipleline (stage 1 and stage 3)
