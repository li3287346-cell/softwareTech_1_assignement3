import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from PIL import Image, ImageTk
from src.config import EDA_OUTPUT_DIR


class MacroApp(tk.Tk):
    """Desktop GUI for displaying EDA outputs."""

    # colours pallete 
    WINDOW_BG = "#f8f9fa"
    PANEL_WHITE = "#ffffff"
    HEADER_PINK = "#c39ea0"
    TEXT_DARK = "#2c3e50"
    TEXT_LIGHT = "#95a5a6"
    INPUT_BG = "#ecf0f1"
    PANEL_BORDER = "#dfe6e9"
    ERROR_RED = "#e74c3c"
    SIDEBAR_BG = "#818D92"
    SELECTED_PINK = "#f8e5e5"

# first method to run
    def __init__(self) -> None:
        super().__init__()
        self.title("Macroinvertebrate EDA Viewer app")
        self.geometry("1500x1200")
        self.configure(bg=self.WINDOW_BG)
        self.resizable(False, False)
    
    # EDA chart options from stage 1 
        self.chart_options = {
            "Class Distribution": "class_distribution.png",
            "Image Size Distribution": "image_size_distribution.png",
            "Sample Image Grid": "sample_grid.png",
            "Box Plot": "boxplot_dimensions.png",
        }
        self.chart_list = list(self.chart_options.keys())
        self.current_index = 0

        self.create_app()

    def create_app (self) -> None:
        self.create_header()

        content = tk.Frame(self, bg=self.WINDOW_BG)
        content.pack(fill="both", expand=True)

        self.create_sidebar(content)
        self.chart_display(content)

    # banner for title 
    def create_header(self) -> None:
        header = tk.Frame(self, bg=self.HEADER_PINK, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Stream Macroinvertebrate EDA",
            font=("Times New Roman", 18, "bold"),
            bg=self.HEADER_PINK,
            fg="white"
        ).pack()

    # Left sidebar with chart buttons and dataset summary.
    def create_sidebar(self, parent) -> None:
        sidebar = tk.Frame(parent, bg=self.SIDEBAR_BG, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # EDA chart title at the top of the side bar 
        
        tk.Label(
            sidebar,
            text="EDA CHARTS",
            font=("Trebuchet MS", 8, "bold"),
            bg=self.SIDEBAR_BG,
            fg="#9ce1df",
            pady=10
        ).pack()
        self.chart_buttons = {}

        charts = [
            ("Class Distribution", "Class Distribution"),
            ("Image Sizes", "Image Size Distribution"),
            ("Sample Grid", "Sample Image Grid"),
            ("Box Plot", "Box Plot"),    
        ]

        for label, key in charts:
            btn = tk.Button(
                sidebar,
                text=label,
                command=lambda k=key: self.select_chart(k),
                font=("Trebuchet MS", 9),
                bg=self.SIDEBAR_BG,
                fg="white",
                activebackground=self.SIDEBAR_BG,
                activeforeground=self.TEXT_DARK,
                relief="flat",
                pady=10,
                cursor="hand2",
                anchor="w",
                padx=16, 
                wraplength=180, 
                justify="left")
            
            btn.pack(fill="x", pady=1)
            self.chart_buttons[key] = btn 

        # Dataset summary
        tk.Label(
            sidebar,
            text="DATASET STATS",
            font=("Trebuchet MS", 8, "bold"),
            bg=self.SIDEBAR_BG,
            fg="#9ce1df",
            pady=6
        ).pack()

        stats = [
            ("Total Images", "2665"),
            ("Total Classes", "17"),
            ("Mean Width", "599 px"),
            ("Mean Height", "390 px"),
        ]

        for label, value in stats:
            stat_frame = tk.Frame(sidebar, bg=self.SIDEBAR_BG)
            stat_frame.pack(fill="x", padx=16, pady=4)

            tk.Label(
                stat_frame,
                text=value,
                font=("Trebuchet MS", 13, "bold"),
                bg=self.SIDEBAR_BG,
                fg="white"
            ).pack(anchor="w")

            tk.Label(
                stat_frame,
                text=label,
                font=("Trebuchet MS", 8),
                bg=self.SIDEBAR_BG,
                fg="#d6eaf8"
            ).pack(anchor="w")
    
    def select_chart(self, key: str) -> None:
        """Highlight the selected button and display the chart."""

        # reset all buttons to default colour
        for k, btn in self.chart_buttons.items():
            btn.configure(bg=self.SIDEBAR_BG, fg="white")

        # button colour changes to pink when selected
        self.chart_buttons[key].configure(
            bg=self.SELECTED_PINK,
            fg=self.TEXT_DARK)

        # display the chart
        self.change_chart(key)

    # display the name of the chart at the top 
    def chart_display (self, parent) -> None:
        main = tk.Frame(parent, bg=self.WINDOW_BG)
        main.pack(side="left", fill="both", expand=True)

        # defualt 
        self.chart_title_label = tk.Label(
            main,
            text="Class Distribution",
            font=("Trebuchet MS", 13, "bold"),
            bg=self.WINDOW_BG,
            fg=self.TEXT_DARK,
            pady=6
        )
        self.chart_title_label.pack(anchor="w", padx=20)

        chart_card = tk.Frame(
            main, bg=self.PANEL_WHITE,
            highlightbackground=self.PANEL_BORDER,
            highlightthickness=1
        )
        chart_card.pack(
            fill="both", expand=True, padx=20, pady=(0, 8)
        )

        self.chart_label = tk.Label(
            chart_card,
            font=("Trebuchet MS", 10),
            bg=self.PANEL_WHITE,
            fg=self.TEXT_LIGHT,
            width=60,
            height=30
        )
        self.chart_label.pack(
            padx=4, pady=4, fill="both", expand=True
        )

        # Navigation and export buttons
        nav_frame = tk.Frame(main, bg=self.WINDOW_BG)
        nav_frame.pack(pady=8)

        tk.Button(
            nav_frame,
            text="Export Chart",
            command=self.export_chart,
            font=("Trebuchet MS", 9, "bold"),
            bg=self.HEADER_PINK,
            fg="white",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2").grid(row=0, column=0, padx=6)

        # Load default chart
        self.select_chart("Class Distribution")


    def change_chart (self, key: str) -> None:
        """Load and display a chart by its key name."""
        self.current_index = self.chart_list.index(key)
        filename = self.chart_options[key]
        chart_path = EDA_OUTPUT_DIR / filename

        self.chart_title_label.configure(text=key)

        if not chart_path.exists():
            self.chart_label.configure(
                image="",
                text=f"Chart not found: {filename}\nRun Stage 1 first.",
                fg=self.ERROR_RED
            )
            self.chart_label.image = None
            return

        image = Image.open(chart_path)
        image.thumbnail((1200, 600))
        photo = ImageTk.PhotoImage(image)
        self.chart_label.configure(image=photo, text="")
        self.chart_label.image = photo
        
    #Save the selected current chart to a location chosen by the user.
    def export_chart(self) -> None:
      
        key = self.chart_list[self.current_index] 
        filename = self.chart_options[key]
        chart_path = EDA_OUTPUT_DIR / filename

        if not chart_path.exists():
            messagebox.showwarning("Not Found", "Chart file not found.")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=filename)
        
        if not save_path:
            return

    # read the chart file and write it to the new location
        with open(chart_path, "rb") as file:
            data = file.read()
        with open(save_path, "wb") as file:
            file.write(data)

        messagebox.showinfo("Saved", f"Chart saved to:\n{save_path}")
