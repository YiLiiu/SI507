import json
import requests
import numpy as np  
import matplotlib.pyplot as plt 
from matplotlib.patches import Polygon  
import random as random 
from matplotlib.path import Path 
import numpy as np 
import re
from collections import Counter
import os
import sys


#step1
redlining_json = requests.get("https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson")
RedliningData = redlining_json.json()
# print(RedliningData)

#step2
class DetroitDistrict:
    def __init__(self, Coordinates = [[[[0,0]]]], HolcGrade = '', HolcColor = '', 
    name = '', Qualitative_Description = '', RandomLat = 0, RandomLong = 0, Median_Income = 0, CensusTract = 0) -> None:
        self.Coordinates = Coordinates
        self.HolcGrade = HolcGrade
        self.HolcColor = HolcColor
        self.name = name
        self.Qualitative_Description = Qualitative_Description
        self.RandomLat = RandomLat
        self.RandomLong =RandomLong
        self.Median_Income = Median_Income
        self.CensusTract = CensusTract

Districts = [DetroitDistrict(Coordinates = RedliningData["features"][i]["geometry"]["coordinates"], 
                             HolcGrade = RedliningData['features'][i]['properties']['holc_grade'], 
                             HolcColor = 'darkgreen' if RedliningData['features'][i]['properties']['holc_grade'] == 'A' 
                            else 'cornflowerblue' if RedliningData['features'][i]['properties']['holc_grade'] == 'B' 
                            else 'gold' if RedliningData['features'][i]['properties']['holc_grade'] == 'C' else 'maroon', 
                            name = i + 1, 
                            Qualitative_Description = RedliningData['features'][i]['properties']['area_description_data']['8']) 
                            for i in range(len(RedliningData["features"]))]

#step3
fig, ax = plt.subplots()
plot_district = []

for i in range(len(RedliningData["features"])):
    polyg = Polygon(Districts[i].Coordinates[0][0], True, edgecolor="black", facecolor=Districts[i].HolcColor)
    plot_district.append(polyg)

for j in plot_district:
    ax.add_patch(j)
    ax.autoscale()
    plt.rcParams["figure.figsize"] = (15,15)

plt.show()

#step7
def fetch_data_with_cache(url, json_cache, params = None) :
    json_data = None
    try:
        with open(os.path.join(sys.path[0], json_cache), 'r') as file:
            json_data = json.load(file)
            for i in json_data:
                if i["input"]["lat"] == params["lat"] and i["input"]["lon"] == params["lon"]:
                    print("Fetch data from cache!")
                    return i
    except(FileNotFoundError, json.JSONDecodeError) as e:
        print(f'No local cache found... ({e})')
    print('Fetching data form url!')
    if params:
        json_data = requests.get(url, params=params).json()
    else:
        json_data = requests.get(url).json()
    json_list.append(json_data)
    return json_data

#step4
random.seed(17) # initialize the random number seed
# arange(start, stop, step) Values are generated within the half-open interval [start, stop), with spacing between values given by step.
xgrid = np.arange(-83.5,-82.8,.004)  # x value
ygrid = np.arange(42.1, 42.6, .004)  # y value
xmesh, ymesh = np.meshgrid(xgrid,ygrid) # generate xy and yx matrix
points = np.vstack((xmesh.flatten(),ymesh.flatten())).T # organize the stack array in row wise

json_list = []
json_cache = 'cache.json'
for j in Districts: 
    # generate line/curve from the value of coordinates and then enclose an area
    p = Path(j.Coordinates[0][0]) 
    # whether the area enclosed by the path contains the given points. 
    grid = p.contains_points(points)  
    print(j," : ", points[random.choice(np.where(grid)[0])])  
    # return a random point in the grid
    point = points[random.choice(np.where(grid)[0])] 
    j.RandomLong = point[0] 
    j.RandomLat = point[1] 
    #step5
    url = 'https://geo.fcc.gov/api/census/area'
    params = {"lat" : j.RandomLat, "lon" : j.RandomLong }
    # response = requests.get(url, params=params)
    # while (response.status_code == 502):
    #     response = requests.get(url, params=params)
    # area_json = json.loads(response.text)
    response = fetch_data_with_cache(url, json_cache, params)
    j.CensusTract = (response["results"][0]["block_fips"][0:11])
if json_list is not None:
    with open(os.path.join(sys.path[0], json_cache), 'w') as f:
        json.dump(json_list, f)

#step6
base_url = 'https://api.census.gov/data/2018/acs/acs5'
income_index = 'B19013_001E'
api_key = 'edc747c4457e8dbb9bc76c874fc431c626a12782'
state = j.CensusTract[0:2]
acs_url = f'{base_url}?get={income_index}&for=tract:*&in=state:{state}&key={api_key}'
response_m = requests.get(acs_url)
m_json = response_m.json()
# print(m_json)

for j in Districts:
    county = j.CensusTract[2:5]
    tract = j.CensusTract[5:11]
    for i in range(len(m_json)):
        if county == m_json[i][2] and tract == m_json[i][3]:
            j.Median_Income = m_json[i][0]


#step8
def cal_mean_income(grade_category):
    total_income = 0
    num_income = 0
    for i in Districts:
        if i.HolcGrade == grade_category:
            if int(i.Median_Income) > 0:
                total_income += int(i.Median_Income)
                num_income += 1
    return total_income / num_income

def cal_median_income(grade_category):
    income_list = []
    for i  in Districts:
        if i.HolcGrade == grade_category:
            if int(i.Median_Income) > 0:
                income_list.append(int(i.Median_Income))
    income_list.sort()
    income_num = len(income_list)
    if income_num % 2 == 0:
        median_income = 0.5 * (float(income_list[income_num // 2]) + float(income_list[income_num // 2 - 1])) 
    else:
        median_income = income_list[income_num // 2]
    return median_income

A_mean_income = cal_mean_income("A")
B_mean_income = cal_mean_income("B")
C_mean_income = cal_mean_income("C")
D_mean_income = cal_mean_income("D")

A_median_income = cal_median_income("A")
B_median_income = cal_median_income("B")
C_median_income = cal_median_income("C")
D_median_income = cal_median_income("D")

print("A_mean_income is "+str(A_mean_income))
print("A_median_income is "+ str(A_median_income))
print("B_mean_income is "+ str(B_mean_income))
print("B_median_income is "+ str(B_median_income))
print("C_mean_income is "+ str(C_mean_income))
print("C_median_income is "+ str(C_median_income))
print("D_mean_income is "+ str(D_mean_income))
print("D_median_income is "+ str(D_median_income))

#step9
ban_words = ['the', 'are', 'of', 'is', 'and', 'this', 'that', 'to', 'it', 'as', 'a', 'but', 'for']
re_ban_words = re.compile(r"\b(" + "|".join(ban_words) + ")\\W", re.I)
def DeleteBannedWords(string):
    return re_ban_words.sub("", string)

sub_A = DeleteBannedWords(''.join([i.Qualitative_Description for i in Districts if i.HolcGrade == 'A']))
sub_B = DeleteBannedWords(''.join([i.Qualitative_Description for i in Districts if i.HolcGrade == 'B']))
sub_C = DeleteBannedWords(''.join([i.Qualitative_Description for i in Districts if i.HolcGrade == 'C']))
sub_D = DeleteBannedWords(''.join([i.Qualitative_Description for i in Districts if i.HolcGrade == 'D']))

pattern = r"[.|,|\s+]"
words_A = re.split(pattern, sub_A)
words_B = re.split(pattern, sub_B)
words_C = re.split(pattern, sub_C)
words_D = re.split(pattern, sub_D)

unique_words_A = [i for i in words_A if i not in words_B and i not in words_C and i not in words_D]
unique_words_B = [i for i in words_B if i not in words_A and i not in words_C and i not in words_D]
unique_words_C = [i for i in words_C if i not in words_A and i not in words_B and i not in words_D]
unique_words_D = [i for i in words_D if i not in words_A and i not in words_B and i not in words_C]

A_10_Most_Common = Counter(unique_words_A).most_common(10)
B_10_Most_Common = Counter(unique_words_B).most_common(10)
C_10_Most_Common = Counter(unique_words_C).most_common(10)
D_10_Most_Common = Counter(unique_words_D).most_common(10)

print(A_10_Most_Common)
print(B_10_Most_Common)
print(C_10_Most_Common)
print(D_10_Most_Common)

# bonus part 1 
fig, ax = plt.subplots()

income_list = []
income_list_real = []
for x in Districts:
  income_list.append(int(x.Median_Income))
for x in income_list:
    if x > 0:
        income_list_real.append(x)
max_incomes = max(income_list)
min_incomes = min(income_list)

patches = []
for i in range(len(RedliningData["features"])):
    edgColor = Districts[i].HolcColor
    if income_list[i] <0:
        polygon = Polygon(Districts[i].Coordinates[0][0], True,facecolor="black", edgecolor = edgColor)
        patches.append(polygon)
    else: 
        intensity = (income_list[i] - min_incomes) / (max_incomes - min_incomes)
        polygon = Polygon(Districts[i].Coordinates[0][0], True, facecolor = plt.get_cmap('Reds')(intensity), edgecolor = edgColor)
        patches.append(polygon)

for x in patches:
    ax.add_patch(x)
    ax.autoscale()
    plt.rcParams["figure.figsize"] = (15,15)
    
plt.show()

# bonus part 2
"""
    The results from part6 supurise me a lot that I never imagine 
    the wealth and poverty divergence in Detroit districts is so big
    that both median/mean income and description has that much difference. 
    These two HW helps me improve the ability of collecting and analysing data,
    and make the data visualization. I have learned a lot about how to utilize 
    the API provided and parse it with regex expression. 
"""