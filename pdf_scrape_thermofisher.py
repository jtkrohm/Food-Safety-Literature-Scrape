import os
import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin

# This is the base URL where the PDFs are located
base_url = 'https://www.thermofisher.com/gd/en/home/industrial/food-beverage/food-beverage-learning-center/food-beverage-resource-library.html'

# The local directory to save downloaded PDFs
local_directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'Food_Beverage_Resources_PDFs')
os.makedirs(local_directory, exist_ok=True)


# Function to download a single PDF file
def download_pdf(file_url, local_directory):
    local_filename = os.path.join(local_directory, file_url.split('/')[-1])
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


# Function to scrape and download all PDFs from the base URL
def scrape_and_download_pdfs(base_url, local_directory):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <a> tags with 'href' attributes containing '.pdf'
    pdf_links = soup.find_all('a', href=lambda x: x and x.endswith('.pdf'))

    for link in pdf_links:
        pdf_url = urljoin(base_url, link['href'])
        try:
            print(f'Downloading {pdf_url}')
            download_pdf(pdf_url, local_directory)
            print(f'Successfully downloaded {pdf_url}')
        except Exception as e:
            print(f'Failed to download {pdf_url}. Reason: {str(e)}')


# Run the script
scrape_and_download_pdfs(base_url, local_directory)