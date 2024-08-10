import logging
import tkinter as tk
from tkinter import messagebox, ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from datetime import datetime


# Set up logging
logging.basicConfig(filename='selenium_test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Dictionary to map website names to URLs and search box names
websites = {
   "Python.org": {"url": "http://www.python.org", "search_box": "q"},
   "Google": {"url": "http://www.google.com", "search_box": "q"},
   "Wikipedia": {"url": "http://www.wikipedia.org", "search_box": "search"},
   "Bing": {"url": "http://www.bing.com", "search_box": "q"}
}


def perform_search(search_term, selected_site):
   site_info = websites[selected_site]
   url = site_info["url"]
   search_box_name = site_info["search_box"]


   # Start the WebDriver and open the website
   try:
       driver = webdriver.Chrome()
       logging.info("WebDriver started successfully.")
       driver.get(url)
       logging.info(f"Website {url} opened successfully.")
   except WebDriverException as e:
       logging.error(f"Error starting WebDriver or opening website: {e}")
       messagebox.showerror("Error", f"Error starting WebDriver or opening website: {e}")
       return


   try:
       # Find the search box and perform the search
       elem = WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.NAME, search_box_name))
       )
       elem.clear()
       elem.send_keys(search_term)
       elem.send_keys(Keys.RETURN)
       logging.info(f"Search for '{search_term}' executed on {selected_site}.")


       # Check if there are results and take a screenshot
       WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.TAG_NAME, "body"))
       )
       assert "No results found." not in driver.page_source
       logging.info("Search results found.")
       # Take a screenshot
       screenshot_path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
       driver.save_screenshot(screenshot_path)
       logging.info(f"Screenshot saved at {screenshot_path}.")
       messagebox.showinfo("Success", f"Search completed successfully. Screenshot saved at {screenshot_path}.")
   except (TimeoutException, AssertionError, NoSuchElementException) as e:
       logging.error(f"Error with search results: {e}")
       messagebox.showerror("Error", f"Error with search results: {e}")
   finally:
       try:
           driver.quit()
       except WebDriverException as e:
           logging.error(f"Error closing WebDriver: {e}")


def start_search():
   search_term = entry.get()
   selected_site = site_combobox.get()
   if search_term and selected_site:
       perform_search(search_term, selected_site)
   else:
       messagebox.showwarning("Input Error", "Please enter a search term and select a website.")


# Set up the Tkinter GUI

root = tk.Tk()
root.title("Selenium Search App - The Pycodes")
root.geometry("400x200")


frame = tk.Frame(root)
frame.pack(padx=10, pady=10)


label = tk.Label(frame, text="Enter search term:")
label.grid(row=0, column=0, padx=5, pady=5)


entry = tk.Entry(frame)
entry.grid(row=0, column=1, padx=5, pady=5)


site_label = tk.Label(frame, text="Select website:")
site_label.grid(row=1, column=0, padx=5, pady=5)


site_combobox = ttk.Combobox(frame, values=list(websites.keys()))
site_combobox.grid(row=1, column=1, padx=5, pady=5)
site_combobox.set("Python.org")  # Set default value


search_button = tk.Button(frame, text="Search", command=start_search)
search_button.grid(row=2, columnspan=2, pady=10)


root.mainloop()
