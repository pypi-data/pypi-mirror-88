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

def main():
  pass

if __name__ == "__main__":
   main()