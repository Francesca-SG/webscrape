import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver 
chromedriver_path = 'C:\\Path\\To\\The\\Webdriver\\executable.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the webpage
url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQzYAQHoAQGIAgGoAgO4AqzVvLUGwAIB0gIkZmNlY2ZkNTYtNTdjNS00N2UzLTk5NzItNTE2YjFlMTkxMjQz2AIF4AIB&sid=05aec3beb8da98175f5ced812bf115b7&aid=304142&ss=United+States&ssne=United+States&ssne_untouched=United+States&lang=en-gb&src=searchresults&dest_id=224&dest_type=country&checkin=2025-01-17&checkout=2025-01-18&ltfd=5%3A1%3A2-2025_1-2025%3A1%3A&group_adults=2&no_rooms=1&group_children=0&nflt=ht_id%3D204%3Bpopular_activities%3D26'
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 40)


# Locate container and "load more" button
try:
    print("Waiting for the container to be present...")
    container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'e01df12ddf d399a62c2a')))
    print("Found the container. Scrolling into view...")
    driver.execute_script("arguments[0].scrollIntoView();", container)
    print("Waiting for the 'load more' button to be clickable...")
    load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'dba1b3bddf e99c25fd33 ea757ee64b f1c8772a7d ea220f5cdc f870aa1234')))
    print("Found the 'load more' button.")
except Exception as e:
    print(f"An error occurred: {e}")
    

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all elements with the specified class
hotel_names = soup.find_all('div', class_='e037993315 f5f8fe25fa')  
hotel_prices = soup.find_all('div', class_='e037993315 ab91cb3011 db9315e4fb0') 

# Initialize list for extracted data
extracted_data = []

# Extract and clean the text from each element
for name, price in zip(hotel_names, hotel_prices):
    hotel_name = name.text.strip()
    hotel_price = price.text.strip()
    extracted_data.append({'Hotel Name': hotel_name, 'Hotel Price': hotel_price})

# Create a DataFrame
df = pd.DataFrame(extracted_data)

# Save the DataFrame to a CSV file
df.to_csv('hotel_data.csv', index=False)

# Print the DataFrame
print(df.head())

# Close the WebDriver
driver.quit()

