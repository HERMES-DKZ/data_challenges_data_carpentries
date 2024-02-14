from bs4 import BeautifulSoup
import urllib.request
import json
import pandas as pd
from datetime import date

# Get current date to specify filenames
today = str(date.today())


## Carpentries Incubator Data


# Get HTML content of URL
with urllib.request.urlopen('https://carpentries.org/community-lessons/#the-carpentries-incubator') as response:
   html = response.read()
   with open('dc_courses'+today+'.html','wb+') as f:
       f.write(html)

# Open html
with open ('dc_courses'+today+'.html', 'rb') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Extract proper script tag and content as string and convert to json dict
noodle_in_soup = soup.body.find('script')
json_data = json.loads(noodle_in_soup.string)

# Transform JSON to DataFrame
df= pd.DataFrame.from_dict(json_data["x"]["tag"]["attribs"]["data"])

# Writing DataFrame to a CSV file
df.to_csv('carpentries_incubator_output'+today+'.csv', index=False)


## Carpentries Lab Data from Github


# Get HTML content of URL
with urllib.request.urlopen('https://api.github.com/orgs/carpentries-lab/repos?page=1&per_page=100') as response:
   data_in_byte = response.read()

lab_data = json.loads(data_in_byte.decode('utf-8'))

# Transform from List to dict
lab_data_dict = {}
x = 0
for i in lab_data:
    lab_data_dict[x] = i
    x = x + 1

# Transform dict to DataFrame
df= pd.DataFrame.from_dict(lab_data_dict, orient='index')

# Writing DataFrame to a CSV File
df.to_csv('carpentries_lab_output'+today+'.csv', index=False)


## Official Carpentries Curricula lessons

# Get JSON content of URL
with urllib.request.urlopen("https://feeds.carpentries.org/lessons.json") as url:
    curriculum_data = json.load(url)

# Transform from list to dict
curriculum_data_dict = {}
x = 0
for i in curriculum_data:
    curriculum_data_dict[x] = i
    x = x + 1

# Transform dict to DataFrame
df= pd.DataFrame.from_dict(curriculum_data_dict, orient='index')

# Writing DataFrame to a CSV File
df.to_csv('carpentries_all_lessons_output'+today+'.csv', index=False)


## Data Carpentries Data from Github 

# Get HTML content of URL

with urllib.request.urlopen('https://api.github.com/orgs/datacarpentry/repos?page=1&per_page=100') as response:
   data_in_byte = response.read()

dc_data = json.loads(data_in_byte.decode('utf-8'))

with urllib.request.urlopen('https://api.github.com/orgs/datacarpentry/repos?page=2&per_page=100') as response:
   data_in_byte = response.read()

dc_data_two = json.loads(data_in_byte.decode('utf-8'))
dc_data.extend(dc_data_two)
print(len(dc_data))

# Transform from list to dict
lab_data_dict = {}
x = 0
for i in dc_data:
    lab_data_dict[x] = i
    x = x + 1

# Transform dict to DataFrame
df= pd.DataFrame.from_dict(lab_data_dict, orient='index')

# Writing DataFrame to a CSV File
df.to_csv('carpentries_datacarpentries_output'+today+'.csv', index=False)
