import requests
import os
from datetime import datetime
import fitz  # PyMuPDF

def download_and_process_pdfs(pdf_links, output_folder):
    visited_links = set()

    def download_pdf(link, folder, count):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                pdf_name = os.path.join(folder, f"pdf_{count}.pdf")
                with open(pdf_name, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                print(f"Downloaded PDF {count}: {pdf_name}")
                return pdf_name
            else:
                print(f"Failed to download PDF {count}. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading PDF {count}: {e}")

    def process_pdf(pdf_path, count):
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(doc.page_count):
                page = doc[page_num]
                links = page.get_links()
                for link in links:
                    url = link.get('uri')
                    if url and url not in visited_links:
                        visited_links.add(url)
                        pdf_links.append(url)
                        print(f"Found additional PDF link in PDF {count}: {url}")

        except Exception as e:
            print(f"Error processing PDF {count}: {e}")

    # Create a folder with the current date as the folder name
    today_folder = os.path.join(output_folder, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(today_folder, exist_ok=True)

    for i, link in enumerate(pdf_links, start=1):
        pdf_path = download_pdf(link, today_folder, i)
        if pdf_path:
            process_pdf(pdf_path, i)

if __name__ == "__main__":
    # Read PDF links from the text file
    with open('your_links.txt', 'r') as file:
        pdf_links = [line.strip() for line in file.readlines()]

    # Replace 'output_folder' with the path to the folder where you want to save the PDFs
    output_folder = 'path/to/your/output/folder'

    download_and_process_pdfs(pdf_links, output_folder)
