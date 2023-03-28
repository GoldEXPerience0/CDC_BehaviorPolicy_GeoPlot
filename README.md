# CDC BehaviorPolicy GeoPlot
## An Interactive Choropleth Map on Health Behaviors and Related Policies in United States

The Centers for Disease Control and Prevention (CDC) provides behavioral risk factors on nutrition, physical activity, and obesity. In addition, they have state legislation and regulations related to these three categories. These are two separate datasets and are in tabular form. To allow others to engage with the data and expand awareness of these risks, I visualized the relevant values on a map with relative magnitudes shown in color for easier comparison. 

![image](https://user-images.githubusercontent.com/12520975/228354561-01548d8f-f3e4-4afb-b1e3-fa995bf6e35f.png)

**Sources:**
1. Nutrition, physical activity, and obesity health behaviors: 
    https://chronicdata.cdc.gov/Nutrition-Physical-Activity-and-Obesity/Nutrition-Physical-Activity-and-Obesity-Behavioral/hn4x-zwk7
    (At the time of the project, the data included the years 2011-2020)
    
2. Legislation regarding nutrition, physical activity, and obesity:
    https://chronicdata.cdc.gov/Nutrition-Physical-Activity-and-Obesity/CDC-Nutrition-Physical-Activity-and-Obesity-Legisl/nxst-x9p4
    (At the time of the project, the data included the years 2001-2017)
    
    Because of the preference of source (1), I joined the data to include all of source (1) but only the years from source (2) that overlapped.
    This made my combined dataset span the years 2011-2020. From source (2), I extracted the relevant enacted policies by state and year.   
    
    It should be noted that there are years where no data was gathered for particular questions, notibly nutrition which only appeared in the latter years. 
    This is evident with a blank map.
    
**How to use:**
1. Select a year with the slider at the top.
2. Choose a topic of obesity, physicial activity, or nutrition with the first drop-down.
3. Then a question within that topic with the second drop-down.
4. If the map shows up, because the data is present, you can hover your cursor over a state.
5. You will be able to read the percentage of population that meets the topic question as well as the number of enacted policies related to the overall topic.

    Note that if there is no data on enacted policies of that state and of that year, it will display as N/A.
