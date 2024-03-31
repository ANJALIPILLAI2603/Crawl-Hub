import threading
import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from threading import Thread
from PIL import Image, ImageTk

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def start_crawling():
    def crawl():
        while links_to_visit and not stop_flag.is_set():
            current_url = links_to_visit.pop(0)
            visited_links.add(current_url)
            status_text.insert(tk.END, f"Visiting: {current_url}\n")
            status_text.see(tk.END)  # Scroll to the end of the text widget
            window.update_idletasks()
            for link in get_links(current_url):
                if link not in visited_links and link not in links_to_visit:
                    links_to_visit.append(link)
        if stop_flag.is_set():
            status_text.insert(tk.END, "Crawling stopped by user.\n")
            status_text.see(tk.END)  # Scroll to the end of the text widget
        else:
            messagebox.showinfo("Crawling Finished", "Web crawling has finished.")

    url = url_entry.get()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a URL.")
        return

    links_to_visit = [url]
    visited_links = set()
    status_text.delete(1.0, tk.END)  # Clear existing text
    status_text.insert(tk.END, "Starting web crawling...\n")
    stop_flag.clear()  # Clear the stop flag
    Thread(target=crawl).start()

def stop_crawling():
    stop_flag.set()

# GUI setup
window = tk.Tk()
window.title("Crawl Hub")


# Convert logo image to PhotoImage
icon_image = Image.open(r"C:\Users\anjal\Desktop\CrawlHub\LOGO.png")
icon_photo = ImageTk.PhotoImage(icon_image)

# Set logo image as window icon
window.iconphoto(True, icon_photo)

# Load and resize the logo
logo_image = Image.open(r"C:\Users\anjal\Desktop\CrawlHub\LOGO.png")
resized_logo = logo_image.resize((180, 165))  # Resize to 100x100
logo_photo = ImageTk.PhotoImage(resized_logo)
logo_label = tk.Label(window, image=logo_photo)
logo_label.pack(pady=10)

url_label = tk.Label(window, text="Enter the URL:")
url_label.pack()

url_entry = tk.Entry(window, width=50)
url_entry.pack(pady=5)

start_button = tk.Button(window, text="Start Crawling", command=start_crawling, bg="green", fg="white", padx=10)
start_button.pack(pady=10)

stop_button = tk.Button(window, text="Stop Crawling", command=stop_crawling, bg="red", fg="white", padx=10)
stop_button.pack(pady=10)

status_text = tk.Text(window, height=20, width=70)
status_text.pack()

stop_flag = threading.Event()

window.mainloop()
