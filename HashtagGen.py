import csv
import boto3
from bs4 import BeautifulSoup
import requests
import random
import cv2

photo = 'dream.jpg'

with open('credentials.csv', 'r') as input:  # download your IAM credentials file from AWS
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]


client = boto3.client('rekognition',
                      aws_access_key_id=access_key_id,          # AWS IAM access_key ID
                      aws_secret_access_key=secret_access_key,  # AWS IAM secret_access_key
                      region_name='eu-west-1')                  # AWS region name

with open(photo, 'rb') as source_image:
    source_bytes = source_image.read()

response = client.detect_labels(Image={'Bytes': source_bytes}, MaxLabels=10)

labels = response['Labels']
output = [dicts for dicts in labels if(dicts['Parents'] == [])]
final = []
for dict in output:
    x = dict['Name']
    y = dict['Confidence']
    final.append([x, y])
print(final)

url = 'https://www.instagram.com/web/search/topsearch/?context=blended&query=%23'

for x in final:
    if '#' in x[0]:
        x[0] = x[0].strip('#')

keyword = final[0][0]
r = requests.get(url + keyword)
response = r.json()['hashtags']
print("FOR : ", keyword)
i = 0

options = [2, 3, 4, 5, 6, 7]
chosenval = random.choice(options)
message = '#'
message += (response[chosenval]['hashtag']['name'])
print(response[chosenval]['hashtag']['name'])
while(cv2.waitKey(1) < 0):
    imagefin = cv2.imread(photo)
    cv2.putText(imagefin, message, (6, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2)
    cv2.imshow("output", imagefin)

