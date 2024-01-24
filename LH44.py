import requests
import os
import re
from datetime import datetime

def download_and_process_pdfs(pdf_links, output_folder):
    visited_links = set()

    def download_pdf(link, folder, count):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                pdf_name = os.path.join(folder, f"{count}.pdf")
                with open(pdf_name, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                print(f"Downloaded PDF {count}: {pdf_name}")
                return pdf_name
            else:
                print(f"Failed to download PDF {count}. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading PDF {count}: {e}")

    def extract_hyperlinks_and_download(pdf_path, count):
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read().decode('latin-1')
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', pdf_content)
                
                for url in urls:
                    if url not in visited_links:
                        visited_links.add(url)
                        pdf_links.append(url)
                        print(f"Found additional PDF link in PDF {count}: {url}")

                        # Download the linked PDF
                        download_folder = os.path.join(output_folder, 'linked_pdfs')
                        os.makedirs(download_folder, exist_ok=True)
                        linked_pdf_name = os.path.join(download_folder, f"{count}_linked.pdf")
                        response_linked = requests.get(url)
                        if response_linked.status_code == 200:
                            with open(linked_pdf_name, 'wb') as linked_pdf_file:
                                linked_pdf_file.write(response_linked.content)
                            print(f"Downloaded linked PDF from {url} to: {linked_pdf_name}")
                        else:
                            print(f"Failed to download linked PDF from {url}. Status Code: {response_linked.status_code}")

        except Exception as e:
            print(f"Error processing PDF {count}: {e}")

    # Create a folder with the current date as the folder name
    today_folder = os.path.join(output_folder, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(today_folder, exist_ok=True)

    for i, link in enumerate(pdf_links, start=1):
        pdf_path = download_pdf(link, today_folder, i)
        if pdf_path:
            extract_hyperlinks_and_download(pdf_path, i)

if __name__ == "__main__":
    # Read PDF links from the text file
    with open('your_links.txt', 'r') as file:
        pdf_links = [line.strip() for line in file.readlines()]

    # Replace 'output_folder' with the path to the folder where you want to save the PDFs
    output_folder = 'path/to/your/output/folder'

    download_and_process_pdfs(pdf_links, output_folder)
