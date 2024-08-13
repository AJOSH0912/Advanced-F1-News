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
