import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from PIL import Image, ImageTk
from data_processing import filter_movies
from visualization import (
    plot_top_movies_embed,
    plot_rating_distribution_embed, plot_yearly_release_embed,
    plot_language_distribution_embed, plot_rating_histogram_embed,
    plot_release_trend_embed, plot_correlation_heatmap_embed,
    plot_bubble_chart_embed, plot_ratings_over_time_embed,plot_top_rated_by_year_embed
)

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movies Analysis")
        self.root.state('zoomed')

        # Background Image
        self.bg_image = Image.open("assets/background.png")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Filter Frame
        self.frame = ttk.Frame(root, bootstyle="dark")
        self.frame.place(relx=0.5, rely=0.05, anchor="n")

        # Chart Frame
        self.chart_frame = ttk.Frame(root, bootstyle="light")
        self.chart_frame.place(relx=0.5, rely=0.25, anchor="n", relwidth=0.92, relheight=0.7)

        # Variables
        self.genre_var = tk.StringVar()
        self.year_min_var = tk.StringVar()
        self.year_max_var = tk.StringVar()

        # Dropdown Options
        self.genres = ["All"]
        self.years = [str(y) for y in range(1980, 2026)]

        # Genre
        ttk.Label(self.frame, text="Genre:", bootstyle="info").grid(row=0, column=0, padx=5)
        self.genre_cb = ttk.Combobox(self.frame, textvariable=self.genre_var, values=self.genres, state="readonly", width=20)
        self.genre_cb.grid(row=0, column=1, padx=5)
        self.genre_cb.set("All")

        # Year Min
        ttk.Label(self.frame, text="Year Min:", bootstyle="info").grid(row=0, column=2, padx=5)
        self.year_min_cb = ttk.Combobox(self.frame, textvariable=self.year_min_var, values=self.years, state="readonly", width=10)
        self.year_min_cb.grid(row=0, column=3, padx=5)
        self.year_min_cb.set("2000")

        # Year Max
        ttk.Label(self.frame, text="Year Max:", bootstyle="info").grid(row=0, column=4, padx=5)
        self.year_max_cb = ttk.Combobox(self.frame, textvariable=self.year_max_var, values=self.years, state="readonly", width=10)
        self.year_max_cb.grid(row=0, column=5, padx=5)
        self.year_max_cb.set("2025")

        # Filter Button
        self.filter_button = ttk.Button(self.frame, text="Apply Filters 🎯", bootstyle="success", command=self.update_movies)
        self.filter_button.grid(row=0, column=6, padx=10)

        # Chart Buttons
        self.chart_buttons_frame = ttk.Frame(root, bootstyle="dark")
        self.chart_buttons_frame.place(relx=0.5, rely=0.17, anchor="n")

        button_data = [
            ("Top Movies", plot_top_movies_embed),
            ("Rating Distribution", plot_rating_distribution_embed),
            ("Yearly Releases", plot_yearly_release_embed),
            ("Language Distribution", plot_language_distribution_embed),
            ("Rating Histogram", plot_rating_histogram_embed),
            ("Release Trend", plot_release_trend_embed),
            ("Correlation Heatmap", plot_correlation_heatmap_embed),
            ("Top Rated by Year", plot_top_rated_by_year_embed),
            ("Bubble Chart", plot_bubble_chart_embed),
            ("Ratings Over Time", plot_ratings_over_time_embed)
        ]

        self.buttons = []
        for idx, (text, func) in enumerate(button_data):
            btn = ttk.Button(
                self.chart_buttons_frame,
                text=text,
                bootstyle="primary-outline",
                command=lambda f=func: f(self.chart_frame, self.movies)
            )
            btn.grid(row=0, column=idx, padx=4, pady=5)
            self.buttons.append(btn)

        # Footer
        self.footer = ttk.Label(root, text="Movies Analyzer - Mayank Fulara", bootstyle="secondary")
        self.footer.pack(side="bottom", pady=5)

        # Initial movie data load
        self.movies = []
        self.update_movies()

    def update_movies(self):
        from tmdb_api import fetch_movies
        all_movies = fetch_movies()

        genre = self.genre_var.get()
        year_min = int(self.year_min_var.get())
        year_max = int(self.year_max_var.get())

        self.movies = filter_movies(all_movies, genre, year_min, year_max)
        plot_top_movies_embed(self.chart_frame, self.movies)


if __name__ == '__main__':
    root = ttk.Window(themename="cyborg") 
    app = MovieApp(root)
    root.mainloop()
