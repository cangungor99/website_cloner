import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from tqdm import tqdm

class SiteCloner:
    def __init__(self, url, clone_type="normal", cookies=None, output_dir="cloned_site", full_mode=False):
        self.url = url
        self.clone_type = clone_type
        self.cookies = cookies
        self.output_dir = output_dir
        self.assets_folder = os.path.join(output_dir, "assets")
        self.full_mode = full_mode
        self.visited_urls = set()
        os.makedirs(self.assets_folder, exist_ok=True)
        self.total_tasks = 1  # Başlangıçta en az 1 sayfa
        self.completed_tasks = 0
    
    def run(self):
        print(f"✅ \033[92mKlon işlemi başladı: {self.url}\033[0m")
        self.clone_page(self.url)
        print("🎉 \033[92mKlonlama tamamlandı!\033[0m")
    
    def update_progress(self):
        self.completed_tasks += 1
        progress = (self.completed_tasks / self.total_tasks) * 100
        print(f"⏳ \033[93mİlerleme: {progress:.2f}% ({self.completed_tasks}/{self.total_tasks})\033[0m")
    
    def clone_page(self, page_url):
        if page_url in self.visited_urls:
            return
        
        self.visited_urls.add(page_url)
        print(f"🔄 \033[94mSayfa indiriliyor: {page_url}\033[0m")
        
        page_content = self.download_page(page_url)
        if page_content:
            soup = BeautifulSoup(page_content, "html.parser")
            self.download_assets(soup)
            self.download_css_imports()
            self.save_page(str(soup), page_url)
            
            if self.full_mode:
                self.find_and_clone_links(soup, page_url)
        
        self.update_progress()
    
    def download_page(self, page_url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(page_url, headers=headers, cookies=self.cookies)
            if response.status_code == 200:
                return response.text
            else:
                print(f"❌ \033[91mSayfa indirilemedi ({response.status_code}): {page_url}\033[0m")
        except Exception as e:
            print(f"❌ \033[91mSayfa indirilemedi: {page_url}, Hata: {e}\033[0m")
        return None
    
    def download_assets(self, soup):
        asset_tags = {'img': 'src', 'link': 'href', 'script': 'src'}
        asset_elements = [element for tag, attr in asset_tags.items() for element in soup.find_all(tag) if element.get(attr)]
        self.total_tasks += len(asset_elements)
        print("🖼️ \033[94mVarlıklar (CSS, JS, img) indiriliyor...\033[0m")
        
        for element in tqdm(asset_elements, desc="Varlıklar İndiriliyor", unit="file"):
            for tag, attr in asset_tags.items():
                asset_url = element.get(attr)
                if asset_url:
                    full_url = urljoin(self.url, asset_url)
                    save_path = os.path.join(self.assets_folder, os.path.basename(urlparse(full_url).path))
                    
                    try:
                        asset_data = requests.get(full_url).content
                        with open(save_path, "wb") as f:
                            f.write(asset_data)
                        print(f"✅ \033[92m{tag.upper()} indirildi: {save_path}\033[0m")
                        element[attr] = os.path.relpath(save_path, self.output_dir)
                    except Exception as e:
                        print(f"❌ \033[91m{full_url} indirilemedi: {e}\033[0m")
            
            self.update_progress()
    
    def download_css_imports(self):
        print("🎨 \033[94mCSS @import bağlantıları kontrol ediliyor...\033[0m")
        for file in os.listdir(self.assets_folder):
            if file.endswith(".css"):
                css_path = os.path.join(self.assets_folder, file)
                with open(css_path, "r", encoding="utf-8") as f:
                    css_content = f.read()
                
                imports = re.findall(r'@import\s+["\'](.*?)["\']', css_content)
                self.total_tasks += len(imports)
                for imp in imports:
                    full_url = urljoin(self.url, imp)
                    save_path = os.path.join(self.assets_folder, os.path.basename(urlparse(full_url).path))
                    
                    try:
                        css_data = requests.get(full_url).content
                        with open(save_path, "wb") as f:
                            f.write(css_data)
                        print(f"✅ \033[92mCSS @import dosyası indirildi: {save_path}\033[0m")
                        css_content = css_content.replace(imp, os.path.relpath(save_path, self.output_dir))
                    except Exception as e:
                        print(f"❌ \033[91m{full_url} indirilemedi: {e}\033[0m")
                    
                    self.update_progress()
                
                with open(css_path, "w", encoding="utf-8") as f:
                    f.write(css_content)
    
    def find_and_clone_links(self, soup, base_url):
        print("🔗 \033[94mSayfadaki linkler taranıyor...\033[0m")
        links = [urljoin(base_url, a_tag["href"]) for a_tag in soup.find_all("a", href=True)]
        self.total_tasks += len(links)
        for link in links:
            parsed_link = urlparse(link)
            parsed_base = urlparse(self.url)
            
            if parsed_link.netloc == parsed_base.netloc and link not in self.visited_urls:
                self.clone_page(link)
    
    def save_page(self, content, page_url):
        os.makedirs(self.output_dir, exist_ok=True)
        filename = "index.html" if page_url == self.url else urlparse(page_url).path.strip("/").replace("/", "_") + ".html"
        file_path = os.path.join(self.output_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ \033[92mSayfa kaydedildi: {file_path}\033[0m")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Web Sayfası Klonlama Aracı")
    parser.add_argument("url", help="Klonlanacak hedef site URL'si")
    parser.add_argument("--type", choices=["normal", "amp"], default="normal", help="Klon türü")
    parser.add_argument("--cookies", help="Kullanılacak cookie (opsiyonel)")
    parser.add_argument("--output", default="cloned_site", help="Çıktı dizini")
    parser.add_argument("--full", action="store_true", help="Tüm siteyi klonla")
    return parser.parse_args()

def main():
    args = parse_arguments()
    cookies = None
    if args.cookies:
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in args.cookies.split(';')}
    
    cloner = SiteCloner(args.url, args.type, cookies, args.output, args.full)
    cloner.run()

if __name__ == "__main__":
    main()