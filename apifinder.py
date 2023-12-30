import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import argparse
import re
from tqdm import tqdm

def download_resources(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        resource_tags = soup.find_all(["link", "script"])

        folder_name = urlparse(url).netloc
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for tag in tqdm(resource_tags, desc="Downloading Resources", unit="file"):
            if tag.name == "link":
                resource_url = tag.get("href")
            elif tag.name == "script":
                resource_url = tag.get("src")
            else:
                continue

            resource_url = urljoin(url, resource_url)

            try:
                resource = requests.get(resource_url)
                if resource.status_code == 200:
                    filename = os.path.join(folder_name, os.path.basename(urlparse(resource_url).path))
                    with open(filename, "wb") as file:
                        file.write(resource.content)
                else:
                    print(f"Failed to download: {resource_url}")  
            except Exception as e:
                print(f"Error downloading {resource_url}: {e}")

def find_api_keys(folder_name):
    api_key_pattern = re.compile(r"[A-Za-z0-9]{30,}")

    api_keys_found = {}

    for subdir, _, files in os.walk(folder_name):
        for file in files:
            file_path = os.path.join(subdir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    potential_keys = api_key_pattern.findall(content)
                    for key in potential_keys:
                        if key not in api_keys_found:
                            api_keys_found[key] = [file_path]
                        else:
                            api_keys_found[key].append(file_path)
            except UnicodeDecodeError:
                # If the file is binary or not in utf-8 encoding, skip reading it as text
                pass

    return api_keys_found

def print_api_keys_with_files(api_keys_found):
    if api_keys_found:
        print("API Keys Found:")
        for key, files in api_keys_found.items():
            print(f"Key: {key}")
            print("Found in:")
            for file in files:
                print(f"- {file}")
            print("-------------------------")
    else:
        print("No API Keys found.")

if __name__ == "__main__":
    print(r"""
           _____ _____   ______ _           _               
     /\   |  __ \_   _| |  ____(_)         | |              
    /  \  | |__) || |   | |__   _ _ __   __| | ___ _ __     
   / /\ \ |  ___/ | |   |  __| | | '_ \ / _` |/ _ \ '__|    
  / ____ \| |    _| |_  | |    | | | | | (_| |  __/ |       
 /_/    \_\_|   |_____| |_|    |_|_| |_|\__,_|\___|_|       
  _                                  ___  __  ___  __  ___  
 | |                                |__ \/_ |/ _ \/_ |/ _ \ 
 | |__  _   _   _ __ ___   __ ___  __  ) || | (_) || | | | |
 | '_ \| | | | | '_ ` _ \ / _` \ \/ / / / | |\__, || | | | |
 | |_) | |_| | | | | | | | (_| |>  < / /_ | |  / / | | |_| |
 |_.__/ \__, | |_| |_| |_|\__,_/_/\_\____||_| /_/  |_|\___/ 
         __/ |                                              
        |___/                                               
    """)
    print(r"""
 __      __  __  __ 
 \ \    / / /_ |/_ |
  \ \  / /   | | | |
   \ \/ /    | | | |
    \  /     | |_| |
     \/      |_(_)_|
                                                                 
    """)
    print("Made with ❤️  by max21910 in 🇫🇷")
    print("Find it on github at :")

    parser = argparse.ArgumentParser(description='Download resources from a website')
    parser.add_argument('-u', '--url', type=str, help='URL of the website', required=True)
    args = parser.parse_args()

    url = args.url
    download_resources(url)

    folder_name = urlparse(url).netloc
    api_keys = find_api_keys(folder_name)

    print_api_keys_with_files(api_keys)