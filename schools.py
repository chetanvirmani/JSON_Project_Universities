"""
Process the JSON file named univ.json. Create 3 maps per instructions below.
The size of the point on the map should be based on the size of total enrollment. Display only those schools 
that are part of the ACC, Big 12, Big Ten, Pac-12 and SEC divisons (refer to valueLabels.csv file)
The school name and the specific map criteria should be displayed when you hover over it.
(For example for Map 1, when you hover over Baylor, it should display "Baylor University, 81%")
Choose appropriate tiles for each map.


Map 1) Graduation rate for Women is over 50%
Map 2) Percent of total enrollment that are Black or African American over 10%
Map 3) Total price for in-state students living off campus over $50,000

"""

import json
import csv

infileJSON = open("univ.json","r")
infileCSV = open("ValueLabels.csv","r")

universityData = json.load(infileJSON)
valueData = csv.reader(infileCSV, delimiter = ",")

valueLabelList = []

leagueList = ["Atlantic Coast Conference", "Big Twelve Conference","Big Ten Conference","Pacific-12 Conference","Southeastern Conference"]

for x in valueData:
    if x[2] in leagueList:
        valueLabelList.append(x[1])



mag1=[]
lon1=[]
lat1=[]
hover1 = []

mag2 = []
lon2 = []
lat2 = []
hover2 = []

mag3 =[]
lon3 = []
lat3 = []
hover3 = []

for x in range(len(universityData)):

    if str(universityData[x]["NCAA"]["NAIA conference number football (IC2020)"]) in valueLabelList and universityData[x]["Graduation rate  women (DRVGR2020)"] > 50:
        mag1.append((universityData[x]["Graduation rate  women (DRVGR2020)"]))
        lon1.append(universityData[x]["Longitude location of institution (HD2020)"])
        lat1.append(universityData[x]["Latitude location of institution (HD2020)"])
        hover1.append((universityData[x]["instnm"])+", "+str(universityData[x]["Graduation rate  women (DRVGR2020)"])+"%")
   
    if str(universityData[x]["NCAA"]["NAIA conference number football (IC2020)"]) in valueLabelList and universityData[x]["Percent of total enrollment that are Black or African American (DRVEF2020)"] > 10:
        mag2.append((universityData[x]["Percent of total enrollment that are Black or African American (DRVEF2020)"]))
        lon2.append(universityData[x]["Longitude location of institution (HD2020)"])
        lat2.append(universityData[x]["Latitude location of institution (HD2020)"])
        hover2.append((universityData[x]["instnm"])+", "+str(universityData[x]["Percent of total enrollment that are Black or African American (DRVEF2020)"])+"%")

    if str(universityData[x]["Total price for in-state students living off campus (not with family)  2020-21 (DRVIC2020)"]).isdigit():
        if str(universityData[x]["NCAA"]["NAIA conference number football (IC2020)"]) in valueLabelList and universityData[x]["Total price for in-state students living off campus (not with family)  2020-21 (DRVIC2020)"] > 50000:
            mag3.append((universityData[x]["Total price for in-state students living off campus (not with family)  2020-21 (DRVIC2020)"]))
            lon3.append(universityData[x]["Longitude location of institution (HD2020)"])
            lat3.append(universityData[x]["Latitude location of institution (HD2020)"])
            hover3.append((universityData[x]["instnm"])+", $"+str("{:,}".format(universityData[x]["Total price for in-state students living off campus (not with family)  2020-21 (DRVIC2020)"])))



from plotly.graph_objects import Scattergeo, Layout
from plotly import offline

data1 = [{
    "type":"scattergeo",
    "lon": lon1, 
    "lat": lat1, 
    "text": hover1, 
    "marker": {
        "size": [mag/3 for mag in mag1],
        "color": mag1,
        "colorscale":"Viridis",
        "reversescale":True,
        "colorbar":{"title":"Percentage"}
        },
    }]

my_layout1 = Layout (title = "Universities with more than 50 percent graduation rate in selected divisions")

fig1 = {"data":data1, "layout": my_layout1}

offline.plot(fig1, filename = "WomenGraduationRate.html")

data2 = [{
    "type":"scattergeo",
    "lon": lon2, 
    "lat": lat2, 
    "text": hover2, 
    "marker": {
        "size": [mag*2 for mag in mag2],
        "color": mag2,
        "colorscale":"Viridis",
        "reversescale":True,
        "colorbar":{"title":"Percentage"}
        },
    }]

my_layout2 = Layout (title = "Universities with over 10 percent of total enrollment represented by Blacks or African Americans in selected divisions")

fig2 = {"data":data2, "layout": my_layout2}

offline.plot(fig2, filename = "BlackOrAfricanAmerican.html")


data3 = [{
    "type":"scattergeo",
    "lon": lon3, 
    "lat": lat3, 
    "text": hover3, 
    "marker": {
        "size": [mag/2500 for mag in mag3],
        "color": mag3,
        "colorscale":"Viridis",
        "reversescale":True,
        "colorbar":{"title":"Price in Dollars"}
        },
    }]

my_layout3 = Layout (title = "Universities with Total price for in-state students living off campus over $50,000 in selected divisions")

fig3 = {"data":data3, "layout": my_layout3}

offline.plot(fig3, filename = "PriceForInStateTuition.html")

