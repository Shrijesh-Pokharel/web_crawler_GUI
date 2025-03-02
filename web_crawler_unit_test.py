import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from web_crawler_GUI import WebCrawler  # Ensure the file is named 'web_crawler_GUI.py'
from urllib.parse import urljoin

class TestWebCrawler(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.output_text = tk.Text(self.root)
        self.output_file = "test_output.txt"
        self.crawler = WebCrawler("http://example.com", 2, self.output_text, self.output_file)
    
    @patch("requests.get")
    def test_crawl(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '''
            <html>
            <head></head>
            <body>
                <a href="/test">Test Link</a>
                <script src="script.js"></script>
            </body>
            </html>
        '''
        mock_response.url = "http://example.com"
        mock_get.return_value = mock_response

        self.crawler.start_crawling()

        expected_link = urljoin("http://example.com", "/test")
        expected_js = urljoin("http://example.com", "script.js")

        self.assertIn(expected_link, self.crawler.links)
        self.assertIn(expected_js, self.crawler.jsfiles)
    
    @patch("requests.get")
    def test_crawl_handles_absolute_and_relative_js(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '''
            <html>
            <head></head>
            <body>
                <script src="https://cdn.example.com/lib.js"></script>
                <script src="/relative.js"></script>
            </body>
            </html>
        '''
        mock_response.url = "http://example.com"
        mock_get.return_value = mock_response

        self.crawler.start_crawling()

        expected_absolute_js = "https://cdn.example.com/lib.js"
        expected_relative_js = urljoin("http://example.com", "/relative.js")

        self.assertIn(expected_absolute_js, self.crawler.jsfiles)
        self.assertIn(expected_relative_js, self.crawler.jsfiles)
    
    def test_log_output(self):
        self.crawler.log_output("Test Output\n")
        content = self.output_text.get("1.0", tk.END)
        self.assertIn("Test Output", content)
    
    def test_print_banner(self):
        self.crawler.print_banner()
        content = self.output_text.get("1.0", tk.END)
        self.assertIn("Recursive Web Crawler", content)
    
    @patch("tkinter.messagebox.showinfo")
    def test_print_results(self, mock_msgbox):
        self.crawler.subdomains.add("http://sub.example.com")
        self.crawler.links.add("http://example.com/page")
        self.crawler.jsfiles.add("http://example.com/script.js")
        self.crawler.print_results()
        
        content = self.output_text.get("1.0", tk.END)
        self.assertIn("http://sub.example.com", content)
        self.assertIn("http://example.com/page", content)
        self.assertIn("http://example.com/script.js", content)
        mock_msgbox.assert_called_once()
    
    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
