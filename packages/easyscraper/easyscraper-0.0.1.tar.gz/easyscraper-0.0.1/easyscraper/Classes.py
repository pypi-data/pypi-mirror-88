import os
import spacy
import requests  
import numpy
import matplotlib.pyplot as plt

from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from spacy.lang.en import English
from textblob import TextBlob

class WordManager:
  def __init__(self):
    pass

  def get_story_text(self):
    with open('story.txt') as file:
      self.story = file.read()

  def get_nouns(self):
    blob = TextBlob(self.story)
    self.nouns = [token[0] for token in blob.tags if token[1]=='NN']

class PictureManager:
  def __init__(self,num_imgs,search_words):
    self.num_imgs = num_imgs
    self.search_words = search_words

  def save_img(self,search_word,img_idx,img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)
    plt.savefig(f'imgs/{search_word}_{img_idx}.png')


  def limit_imgs(self,all_imgs):

      num_total_imgs = len(all_imgs)

      self.img_urls=[]

      for img in all_imgs[:min(num_total_imgs-1,2*self.num_imgs)]:

        try:
          self.img_urls += [img['src']]

        except:
          continue


  def get_html(self,search_word):

      search_url = f'https://images.search.yahoo.com/search/images;_ylt=AwrExdrB_MlfwyYAsv6LuLkF;_ylc=X1MDOTYwNTc0ODMEX3IDMgRmcgMEZ3ByaWQDc0cuQS5iMU9ScGl0aVlTNFlUUnBrQQRuX3N1Z2cDMTAEb3JpZ2luA2ltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzYEcXVlcnkDcmFtYmFuBHRfc3RtcAMxNjA3MDcyOTY2?fr2=sb-top-images.search&p={search_word}&ei=UTF-8&iscqry=&fr=sfp'

      htmldata =  requests.get(search_url).text

      soup = BeautifulSoup(htmldata, 'html.parser')  

      self.all_imgs = soup.find_all('img')


  def make_img_dir(self):

    folder_name = 'imgs'

    if not os.path.exists(folder_name):

      os.mkdir(folder_name)


  def get_imgs(self):

    self.make_img_dir()

    for search_word in self.search_words:

      self.get_html(search_word)

      self.limit_imgs(self.all_imgs)

      for img_idx,img_url in enumerate(self.img_urls[:self.num_imgs]):
          
          self.save_img(search_word,img_idx,img_url)


def main():
  pass

if __name__ == "__main__":
   main()