import os

from dotenv import load_dotenv
from imgurpython import ImgurClient

load_dotenv()

class ImageService:
    def __init__(self):
        self.__client_id = os.getenv('imgur_client_id')
        self.__client_secret = os.getenv('imgur_client_secret')
        self.__client = ImgurClient(self.__client_id, self.__client_secret)

    def get_image(self, id: str) -> str | None:
        if id is None:
            return None
        else:
            return f'https://i.imgur.com/{id}.png'

    def get_album(self, id: int) -> list[str] | list[None] | None:
        links_list = []
        if id is None:
            return [None]
        else:
            try:
                with open('.img_cache', 'r') as cache_file:
                    for entry in cache_file:
                        if entry.startswith(id):
                            links = entry[entry.find('[')+1:entry.find(']')]
                            links_list = [link.strip().strip("'") for link in links.split(',')]
                            return links_list
                items = self.__client.get_album_images(id)
                for item in items:
                    links_list.append(item.link)
                with open('.img_cache', 'a') as cache_file:
                    cache_file.write(f"{id}, {str(links_list)}\n")
            except:
                return None
        return links_list