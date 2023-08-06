#brightness_4
# Python program to generate WordCloud

# importing all necessery modules
from sentencecloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import cv2

#Load teammember details
a_file = open("/Users/rajesh.prabhu/PycharmProjects/WordCloudRaj/venv/bin/abc.csv", "r")
list_of_sentences = [(line.strip()) for line in a_file]
a_file.close()

#Generate Strength Sentence Frequency List
strength_frequency = {}
count = 30
iter_num = 0
for sentence in list_of_sentences:
    iter_num+=1
    strength_frequency[sentence] = count
    count = 22 if iter_num == 1 else 12 if iter_num ==2 else 7 if iter_num ==3 else 4 if iter_num == 4 else 7-iter_num
    if count < 2:
        count=1


#Select Cloud Shape (mask)
sentences = len(list_of_sentences)
maskname = 'jetfighter.jpg' if sentences > 25 else 'diamond.jpg' if sentences > 20 else 'oval.jpg' if sentences > 15 else 'diamond.jpg'
custom_mask = np.array(Image.open(r"/Users/rajesh.prabhu/PycharmProjects/WordCloudRaj/venv/bin/jetfighter.jpg"))

#########"+maskname

#Generate Cloud
wordcloud = WordCloud(width=1000, height=1000,
                      background_color='black',
                      min_font_size=20,
                      max_font_size=400,
                      mask=custom_mask).generate(strength_frequency)

#""" debug - display on screen
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
#"""

#save to file
sent_cloud=np.array(np.rot90(wordcloud,-1))
cv2.imwrite('/Users/rajesh.prabhu/PycharmProjects/WordCloudRaj/venv/bin/sentcloud.png', sent_cloud)
#"""


