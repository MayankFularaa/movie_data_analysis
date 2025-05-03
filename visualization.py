import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import pandas as pd

plt.style.use('dark_background')

# Embedding chart in Tkinter Frame
def embed_chart(fig, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    fig.patch.set_alpha(0.0) 
    fig.subplots_adjust(left=0.2, bottom=0.2, right=0.95, top=0.85)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill="both", padx=20, pady=20)
    canvas_widget.configure(bg='#000000', highlightthickness=0)

# Set dark theme for axes
def apply_dark_theme(ax):
    ax.set_facecolor('none')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')


def plot_top_movies_embed(frame, movies, top_n=10):
    titles = [movie['title'] for movie in movies[:top_n]]
    ratings = [movie.get('vote_average', 0) for movie in movies[:top_n]]

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.barh(titles[::-1], ratings[::-1], color='skyblue')
    ax.set_title(f"Top {top_n} Rated Hindi Movies")
    ax.set_xlabel("Rating")
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_genre_distribution_embed(frame, movies):
    all_genres = []
    for movie in movies:
        genres = movie.get("genre", "")
        if isinstance(genres, str):
            genres = [g.strip() for g in genres.split(',') if g.strip()]
        all_genres.extend(genres)

    genre_counts = Counter(all_genres)
    if not genre_counts:
        tk.Label(frame, text="No genres to display", bg="#222", fg="white").pack()
        return

    genres, counts = zip(*genre_counts.most_common(10))
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=list(counts), y=list(genres), ax=ax, palette="magma")
    ax.set_title("Top Genres Distribution")
    ax.set_xlabel("Count")
    ax.set_ylabel("Genre")
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_rating_distribution_embed(frame, movies):
    ratings = [movie.get('vote_average', 0) for movie in movies]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(ratings, bins=10, color='purple', edgecolor='white')
    ax.set_title("Rating Distribution")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_yearly_release_embed(frame, movies):
    years = [int(movie['release_date'][:4]) for movie in movies if movie.get('release_date')]
    year_counts = Counter(years)
    sorted_years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in sorted_years]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sorted_years, counts, marker='o', color='lime')
    ax.set_title("Movie Releases Over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_ratings_over_time_embed(frame, movies, window=5):
    data = [(int(m['release_date'][:4]), m['vote_average']) for m in movies if m.get('release_date')]
    df = pd.DataFrame(data, columns=['year', 'rating'])
    df = df.groupby('year')['rating'].mean().reset_index()
    df['moving_avg'] = df['rating'].rolling(window=window).mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['year'], df['rating'], label='Average Rating', color='cyan')
    ax.plot(df['year'], df['moving_avg'], label=f'{window}-Year Moving Average', color='orange')
    ax.legend(facecolor='none', edgecolor='white', labelcolor='white')
    ax.set_title("Ratings Over Time with Moving Average")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rating")
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_bubble_chart_embed(frame, movies):
    ratings = [m.get('vote_average', 0) for m in movies]
    popularity = [m.get('popularity', 0) for m in movies]
    votes = [m.get('vote_count', 0) for m in movies]

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(popularity, ratings, s=[v/10 for v in votes], alpha=0.6, c=ratings, cmap='viridis')
    ax.set_title('Popularity vs Rating vs Vote Count')
    ax.set_xlabel('Popularity')
    ax.set_ylabel('Rating')
    plt.colorbar(scatter, ax=ax, label='Rating')
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_correlation_heatmap_embed(frame, movies):
    data = {
        'vote_average': [movie.get('vote_average', 0) for movie in movies],
        'popularity': [movie.get('popularity', 0) for movie in movies],
        'vote_count': [movie.get('vote_count', 0) for movie in movies]
    }
    df = pd.DataFrame(data)
    corr = df.corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Heatmap')
    apply_dark_theme(ax)
    embed_chart(fig, frame)

def plot_language_distribution_embed(frame, movies):
    lang_counter = Counter([movie.get('original_language', 'unknown') for movie in movies])
    langs = list(lang_counter.keys())
    counts = list(lang_counter.values())

    fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')  # Transparent background
    ax.bar(langs, counts, color='orange')
    ax.set_title('Language Distribution')
    ax.set_xlabel('Language')
    ax.set_ylabel('Count')
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_rating_histogram_embed(frame, movies):
    ratings = [movie.get('vote_average', 0) for movie in movies]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')  # Transparent background
    ax.hist(ratings, bins=10, color='teal', edgecolor='black')
    ax.set_title('Histogram of Movie Ratings')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_release_trend_embed(frame, movies):
    years = [int(movie['release_date'][:4]) for movie in movies if movie.get('release_date')]
    year_counts = Counter(years)
    sorted_years = sorted(year_counts)
    counts = [year_counts[year] for year in sorted_years]

    fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')  # Transparent background
    ax.plot(sorted_years, counts, marker='o', linestyle='-', color='cyan')
    ax.set_title('Movie Release Trend Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Movies Released')
    apply_dark_theme(ax)
    embed_chart(fig, frame)


def plot_top_rated_by_year_embed(frame, movies):
    from collections import defaultdict
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    for widget in frame.winfo_children():
        widget.destroy()

    year_movies = defaultdict(list)
    for movie in movies:
        year = movie.get('release_date', '')[:4]
        if year and movie.get('vote_average', 0) > 0:
            year_movies[year].append(movie)

    top_per_year = []
    for year, mvs in year_movies.items():
        top_movie = max(mvs, key=lambda x: x['vote_average'])
        top_per_year.append((year, top_movie['title'], top_movie['vote_average']))

    top_per_year.sort(key=lambda x: x[0])  # Sort by year

    years = [t[0] for t in top_per_year]
    ratings = [t[2] for t in top_per_year]

    fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')
    ax.plot(years, ratings, marker='o', linestyle='-', color='tomato')
    ax.set_title('Top Rated Movie by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Rating')
    plt.xticks(rotation=45)

    apply_dark_theme(ax)
    embed_chart(fig, frame)

