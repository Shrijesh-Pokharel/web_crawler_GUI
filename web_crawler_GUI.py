import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin


class WebCrawler:
    def __init__(self, url, max_depth, output_text_widget, output_file):
        self.url = url
        self.max_depth = max_depth
        self.subdomains = set()
        self.links = set()
        self.jsfiles = set()
        self.output_text = output_text_widget
        self.output_file = output_file

    def start_crawling(self):
        self.crawl(self.url, depth=1)

    def crawl(self, url, depth):
        if depth > self.max_depth:
            return

        try:
            response = requests.get(url, timeout=3, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as err:
            self.log_output(f"[-] An error occurred: {err}\n")
            return

        subdomain_query = fr"https?://([a-zA-Z0-9.-]+)"

        for link in soup.find_all('a'):
            link_text = link.get('href')
            if link_text:
                if re.match(subdomain_query, link_text) and link_text not in self.subdomains:
                    self.subdomains.add(link_text)
                else:
                    full_link = urljoin(url, link_text)
                    if full_link != url and full_link not in self.links:
                        self.links.add(full_link)
                        self.crawl(full_link, depth + 1)

        for file in soup.find_all('script'):
            script_src = file.get('src')
            if script_src:
                full_script_url = urljoin(url, script_src)
                self.jsfiles.add(full_script_url)

    def log_output(self, text):
        self.output_text.insert(tk.END, text)
        with open(self.output_file, "a", encoding="utf-8") as file:
            file.write(text)

    def print_banner(self):
        banner_text = "-" * 80 + "\n"
        banner_text += f"Recursive Web Crawler starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        banner_text += "-" * 80 + "\n"
        banner_text += f"[*] URL : {self.url}\n"
        banner_text += f"[*] Max Depth : {self.max_depth}\n"
        banner_text += "-" * 80 + "\n"
        self.log_output(banner_text)

    def print_results(self):
        if self.subdomains:
            for subdomain in self.subdomains:
                self.log_output(f"[+] Subdomains : {subdomain}\n")

        if self.links:
            for link in self.links:
                self.log_output(f"[+] Links : {link}\n")

        if self.jsfiles:
            for file in self.jsfiles:
                self.log_output(f"[+] JS Files : {file}\n")

        messagebox.showinfo("Task Completed", "Web Crawling Task has been completed successfully!")


def start_crawl():
    url = url_entry.get()
    try:
        depth = int(depth_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid depth value.")
        output_text.insert(tk.END, "[-] Invalid depth value.\n")
        return

    if not url:
        messagebox.showerror("Invalid Input", "Please enter a URL.")
        output_text.insert(tk.END, "[-] Please enter a URL.\n")
        return

    output_text.delete(1.0, tk.END)
    output_file = "crawl_output.txt"
    open(output_file, "w").close()

    web_crawler = WebCrawler(url, depth, output_text, output_file)
    web_crawler.print_banner()
    web_crawler.start_crawling()
    web_crawler.print_results()

 
root = tk.Tk()
root.title("Web Crawler GUI")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

depth_label = tk.Label(root, text="Enter Depth:")
depth_label.pack(pady=5)
depth_entry = tk.Entry(root, width=50)
depth_entry.pack(pady=5)

submit_button = tk.Button(root, text="Start Crawling", command=start_crawl)
submit_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(pady=5)

root.mainloop()
