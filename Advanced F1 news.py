import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

#Personal API key (PLEASE DO NOT USE)
API_KEY = "2fcff62f7450495c9bb8056bc42203c0"
NEWS_API_URL = "https://newsapi.org/v2/everything"

class F1NewsApp: #Creating a class for the F1 News App
    def __init__(self, root): #Initialising the class
        self.root = root
        self.root.title("News") #creates Title of the app
        self.page = 1
        self.page_size = 5
        self.query = "Formula 1 OR F1" #ORiginal Query
        self.sort_by = "publishedAt"
        self.from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d') #Date from 7 days ago
        self.to_date = datetime.now().strftime('%Y-%m-%d')
        self.saved_articles = []# List fo saved articles
        self.setup_gui()
        self.fetch_and_display_news()#Fetches and displays news

    def setup_gui(self): #Setting up the GUI
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(filter_frame, text="Search:").grid(row=0, column=0, sticky="w")
        self.search_entry = ttk.Entry(filter_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.insert(0, self.query)
        ttk.Label(filter_frame, text="Sort by:").grid(row=0, column=2, sticky="w", padx=5)
        self.sort_by_combo = ttk.Combobox(filter_frame, values=["publishedAt", "relevancy", "popularity"], state="readonly")
        self.sort_by_combo.set(self.sort_by)
        self.sort_by_combo.grid(row=0, column=3, padx=5)
        ttk.Label(filter_frame, text="From date:").grid(row=0, column=4, sticky="w", padx=5)
        self.from_date_entry = ttk.Entry(filter_frame, width=10)
        self.from_date_entry.grid(row=0, column=5, padx=5)
        self.from_date_entry.insert(0, self.from_date)

        ttk.Label(filter_frame, text="To date:").grid(row=0, column=6, sticky="w", padx=5)
        self.to_date_entry = ttk.Entry(filter_frame, width=10)
        self.to_date_entry.grid(row=0, column=7, padx=5)
        self.to_date_entry.insert(0, self.to_date)
        search_button = ttk.Button(filter_frame, text="Search", command=self.fetch_and_display_news) #Creates tge search button
        search_button.grid(row=0, column=8, padx=10)
        self.dark_mode = tk.BooleanVar()
        theme_toggle = ttk.Checkbutton(filter_frame, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme)
        theme_toggle.grid(row=0, column=9, padx=10)
        self.news_frame = ttk.Frame(self.root)
        self.news_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.news_canvas = tk.Canvas(self.news_frame)
        self.scroll_y = ttk.Scrollbar(self.news_frame, orient="vertical", command=self.news_canvas.yview)
        self.scroll_frame = ttk.Frame(self.news_canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.news_canvas.configure(
                scrollregion=self.news_canvas.bbox("all")
            )
        )

#The following code above is for formating, it creates the gui and places the buttons and labels in the correct place. it also assigns the correct functions to the buttons.
        self.news_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw") #mkes a window for the news
        self.news_canvas.configure(yscrollcommand=self.scroll_y.set)
        self.news_canvas.pack(side="left", fill="both", expand=True) 
        self.scroll_y.pack(side="right", fill="y")
        pagination_frame = ttk.Frame(self.root)
        pagination_frame.pack(fill="x", padx=10, pady=10)
        self.prev_button = ttk.Button(pagination_frame, text="Previous", command=self.previous_page)
        self.prev_button.pack(side="left")
        self.page_label = ttk.Label(pagination_frame, text=f"Page {self.page}")
        self.page_label.pack(side="left", padx=10)
        self.next_button = ttk.Button(pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="right")
        saved_button = ttk.Button(pagination_frame, text="View Saved Articles", command=self.view_saved_articles)
        saved_button.pack(side="left", padx=10)
#The following code above creates the page thingy buttons and the saved articles button. 
    def fetch_news(self): #Function to fetch news
        query = self.search_entry.get()
        sort_by = self.sort_by_combo.get()
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        query_params = {
            "q": query,
            "apiKey": API_KEY,
            "language": "en",
            "sortBy": sort_by,
            "from": from_date,
            "to": to_date,
            "pageSize": self.page_size,
            "page": self.page
        }
        response = requests.get(NEWS_API_URL, params=query_params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return articles
        else:
            messagebox.showerror("Error", f"Failed to fetch news: {response.status_code}")
            return []
        
#The following code above fetches the news from the API and returns the articles