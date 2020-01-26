from selenium.webdriver.firefox.options import Options
import shutil, requests, hashlib, os, time, ctypes, pickle
import random as rnd
from selenium import webdriver
from bs4 import BeautifulSoup
from cv2 import imread, IMREAD_UNCHANGED

class WallpaperManager():

    def __init__(self, directory='Images', random=True, delay=10):
        self.options = Options()
        self.options.headless = True
        self.directory = directory
        self.random = random
        self.delay = delay

        if 'images.cache' in [i for i in os.listdir()]:
            self.downloaded_images = pickle.load( open( "images.cache", "rb" ) )
        else:
            self.downloaded_images = []

    def getwallpapers(self, download=True):
        self.browser = webdriver.Firefox(options=self.options)
        self.url = 'https://unsplash.com/s/photos/wallpapers-hd'
        self.browser.get(self.url)
        for i in reversed(range(int(random.random()*10))):
            content = self.browser.page_source
            soup = BeautifulSoup(content, "lxml")
            for image in soup.find_all('img'):
                if image.get('src').startswith('https://images.unsplash.com/photo'):
                    if download:
                        self.download_image(image.get('src'))
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1." + str(i) + ");")
            time.sleep(int(random.random()*10))
        self.browser.quit()

    def download_image(self, url):
        with requests.get(url, stream=True) as response:
            images = [i for i in os.listdir() if i.endswith('.png')]
            if hashlib.sha256(url.encode('utf-8')).hexdigest()+'.png' in images:
                print('this image was already downloaded')
            else:
                print('Downlaoding an image...')

                image = hashlib.sha256(url.encode('utf-8')).hexdigest()+'.png'

                with open(image, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

                directory = os.getcwd() + '\\' + self.directory + '\\'
                try:
                    os.rename(os.getcwd() + '\\' + image, directory + self.get_hash(image))
                except FileNotFoundError:
                    os.system('mkdir ' + self.directory)
                    time.sleep(1)
                    os.rename(os.getcwd() + '\\' + image, directory + self.get_hash(image))
                except FileExistsError:
                    pass
                finally:
                    self.downloaded_images.append(image)
                    pickle.dump(self.downloaded_images, open( "images.cache", "wb" ) )

    def get_hash(self, filename):
        sha256_hash = hashlib.sha256()
        with open(filename,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()

    def set_wallpaper(self, image_path):

        img = imread(image_path, IMREAD_UNCHANGED)

        if (img.shape[0] < img.shape[1]) and (img.shape[0] >= 700): #if the width is bigger than the height
            if ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3):
                print('height',img.shape[0],',','width',img.shape[1])
                return True
        else:
            os.remove(image_path.split('\\')[len(image_path.split('\\'))-1])

    def set_random_wallpaper(self, random=True, delay=10):
        images = [i for i in os.listdir(self.directory) if i.endswith('.png')]
        if len(images) == 0:
            self.getwallpapers()
        if random:
            rnd.shuffle(images)
        for image in reversed(images):
            self.set_wallpaper(os.getcwd() + '\\' + self.directory + '\\' + image)
            time.sleep(delay)


def main():

    manager = WallpaperManager()
    manager.set_random_wallpaper()

if __name__ == '__main__':
    main()
