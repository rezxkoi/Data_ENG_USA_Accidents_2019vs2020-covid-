'''
Make sure to install streamlit with `conda install -c conda-forge streamlit`.

Run `streamlit hello` to get started!

Streamlit is *V* cool, and it's only going to get cooler (as of February 2021):

https://discuss.streamlit.io/t/override-default-color-palette/9088/2

To run this app, run `streamlit run streamlit_app.py` from inside this directory
'''


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import streamlit as st
import streamlit.components.v1 as components


# PART 3
#st.image("traffic_pic.jpeg", use_column_width=False#)

st.set_page_config(layout="wide")
st.title(
'''
UNITED STATES YEARLY ACCIDENTS CHARTS & VISUALIZATIONS  


''')
st.write('''
The dataset used here for exploratory data analysis is "USA Accidents" - A Countrywide Traffic Accident Dataset (2019 & 2020) from www.kaggle.com. Each dataset is explored seperatly for better understanding of the accidnets.

US-Accidents can be used for numerous applications such as real-time car accident prediction, studying car accidents hotspot locations, casualty analysis and extracting cause and effect rules to predict car accidents, and studying the impact of precipitation or other environmental stimuli on accident occurrence.
''')
data_list = ['USA Accidents Data 2019','USA Accidents Data 2020'] 
USA_Accidents_Data_2019 = 'us_accide_2019.csv'
USA_Accidents_Data_2020 = 'usa_accidents_2020.csv'

dataset_name = st.selectbox(label='Select Dataset:',options= data_list)
#data = pd.read_csv('us_accide_2019.csv')
#data = data.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})
#st.dataframe(data)

def get_dataset(dataset_name):
    if dataset_name == 'USA Accidents Data 2019':
        data = pd.read_csv('us_accide_2019.csv')
    if dataset_name == 'USA Accidents Data 2020':
        data = pd.read_csv('usa_accidents_2020.csv')
    return data
data = get_dataset(dataset_name)

def data_year(dataset_name):
    if dataset_name == 'USA Accidents Data 2019':
        year = '2019'
    if dataset_name == 'USA Accidents Data 2020':
        year = '2020'
    return year
year = data_year(dataset_name)

def accident_count(dataset_name):
    if dataset_name == 'USA Accidents Data 2019':
        acc_count = data.shape
    if dataset_name == 'USA Accidents Data 2020':
        acc_count = data.shape
    return str(acc_count[0])
number_of_accidents = accident_count(dataset_name)

#number_of_accidents = data.shape

st.write(''' ### Total Accidents:'''  )

st.write('''

Total accidents recorded all around USA in year '''f"{year}" +':'+  f"**{number_of_accidents}**" )





# PART 4

st.write(
'''
### Graphs & Visualizations
##### Top 10 cities with highest number of accidents:
'''
)

#Bar Chart to Visualize Top 10 cities by number of accidents
accidents_by_cities = data['City'].value_counts()
#accidents_by_cities[:10]
fig1, ax1 = plt.subplots(figsize=(16,5))
accidents_by_cities[:10].plot(kind='barh')
ax1.set(title = 'Top 10 cities By Number of Accidents',
       xlabel = 'Cities',
       ylabel ='Accidents Count')
show_graph1 = st.checkbox('Show Graph', value=True,key="1")

if show_graph1:
    st.pyplot(fig1)


st.write(
'''

##### Top 10 states with highest number of accidents:
'''
)

#Bar Chart to Visualize Top 10 states by number of accidents
accidents_by_states = data['State'].value_counts()

fig2, ax2 = plt.subplots(figsize=(16,5))
accidents_by_states[:10].plot(kind='barh')
ax2.set(title = 'Top 10 states By Number of Accidents',
       xlabel = 'States',
       ylabel = 'Accidents Count')
show_graph2 = st.checkbox('Show Graph', value=True,key="2")

if show_graph2:
    st.pyplot(fig2)


st.write(
'''
##### Accidents severity proportion between severity classes:

- Severity Level 1: No Injuries, No travel lanes blocked 
- Severity Level 2: Minor Injuries and/or 1 travel lane blocked  
- Severity Level 3: Serious injuries or 2 or more travel lanes blocked 
- Severity Level 4: Multiple agencies needed, HAZMAT spill, threat to life and property extends beyond the confines of the traffic incident scene, or ALL LANES BLOCKED



'''
)

# Let's visualize accident severity distribution
accidents_severity = data.groupby('Severity').count()['ID']
fig3, ax3 = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"))
def num_severity_labels(dataset_name):
    if dataset_name == 'USA Accidents Data 2019':
        label = [2,3,4]
    if dataset_name == 'USA Accidents Data 2020':
        label = [1,2,3,4]
    return label
label_sev = num_severity_labels(dataset_name)
plt.pie(accidents_severity, labels=label_sev,
        autopct='%1.1f%%', pctdistance=0.85)
circle = plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(circle)
ax3.set_title("Accident by Severity",fontdict={'fontsize': 12})
show_graph3 = st.checkbox('Show Graph', value=True,key="3")

if show_graph3:
    st.pyplot(fig3)


st.write(
'''

##### Accidents in relation with time of the day:
'''
)
# Let's work with the dates 
# (we find it's in wrong format, let's change that)


data = data.astype({'Start_Time': 'datetime64[ns]', 'End_Time': 'datetime64[ns]'})

# Plot the distribution of occurence by time of the day.
# We can see the time of the day mof accidents happen, 4pm-6pm

fig4, ax4 = plt.subplots(figsize=(16,8))
sns.histplot(data['Start_Time'].dt.hour, bins = 24)

plt.xlabel("Start Time")
plt.ylabel("Number of Occurence")
plt.title('Accidents Count By Time of Day')

show_graph4 = st.checkbox('Show Graph', value=True,key="4")

if show_graph4:
    st.pyplot(fig4)


st.write(
'''

##### Accidents in relation to day of the week:
'''
)
# Let's plot by day of the week 

fig5, ax5 = plt.subplots(figsize=(16,5))
sns.histplot(data['Start_Time'].dt.dayofweek, bins = 7)

plt.xlabel("Day of Week")
plt.ylabel("Occurence")
plt.title('Accidents Occurence by Day of the Week')

show_graph5 = st.checkbox('Show Graph', value=True,key="5")

if show_graph5:
    st.pyplot(fig5)


st.write()


st.write(
'''

##### Accidents in relation to months of the year:
'''
)
#Moving on, we can plot by month of the year

fig6, ax6 = plt.subplots(figsize=(16,5))
sns.histplot(data['Start_Time'].dt.month, bins = 12)

plt.xlabel("Month of Year")
plt.ylabel("Accidents Occurence")
plt.title('Accidents Occurence by Month of the Year')

show_graph6 = st.checkbox('Show Graph', value=True,key="6")

if show_graph6:
    st.pyplot(fig6)


st.write(
'''

##### Proportion of accidents happening on the "Right" or "Left" side of the road:
'''
)

# Moving on, what side of the road are accidents happening?

side_of_road =  data.groupby(['Side']).count()['ID']
#Let's visualize that

fig7, ax7 = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"))
side = ['Left', 'Right']
plt.pie(side_of_road, labels=side,
        autopct='%1.1f%%', pctdistance=0.85)
circle = plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(circle)
ax7.set_title("Accident Occurence by Side of Road",fontdict={'fontsize': 16})
show_graph7 = st.checkbox('Show Graph', value=True,key="7")

if show_graph7:
    st.pyplot(fig7)


st.write(
'''

##### Accidents with respect to weather conditions:
'''
)

# What are the weather conditions at the time of accicent occurence

weather_conditions = data.groupby(['Weather_Condition']).count()['ID']
fig8, ax8 = plt.subplots(figsize=(16,8))
weather_conditions.sort_values(ascending=False)[:10].plot(kind='barh')
ax8.set(title = 'Weather Conditions at Time of Accident Occurence',
       xlabel = 'Weather',
       ylabel = 'Accidents Count')
show_graph8 = st.checkbox('Show Graph', value=True,key="8")

if show_graph8:
    st.pyplot(fig8)


st.write(
'''
##### Accidents by longitude-lattutude(Severity & Number of Accidents):
'''
)

def main():
    def html_temp(dataset_name):
        if dataset_name == 'USA Accidents Data 2019':
            html_tab = """
                    <div class='tableauPlaceholder' id='viz1639725540039' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='accidents2019&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1639725540039');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='650px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='650px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        if dataset_name == 'USA Accidents Data 2020':
            html_tab = "<div class='tableauPlaceholder' id='viz1639687304158' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='usa-accidents&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1639687304158');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='850px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='687px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='850px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='687px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
        return html_tab
    components.html(html_temp(dataset_name),width=900,height=600)

if __name__ == "__main__":    
    main()




st.write(
'''
##### Accidents by longitude-lattutude(Heatmap):
'''
)

sample_df = data.sample(int(0.001 * len(data)))
lat_lon_pairs = list(zip(list(sample_df.Start_Lat), list(sample_df.Start_Lng)))
map = folium.Map(width=800,height=500)
HeatMap(lat_lon_pairs).add_to(map)
folium_static(map)





# "# streamlit-folium"

# with st.echo():
#     import streamlit as st
#     from streamlit_folium import folium_static
#     import folium

#     # center on Liberty Bell
#     m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

#     # add marker for Liberty Bell
#     tooltip = "Liberty Bell"
#     folium.Marker(
#         [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
#     ).add_to(m)

#     # call to render Folium map in Streamlit
#     folium_static(m)
# col1, col2 = st.columns(2)

# with col1:
#     sample_df = data.sample(int(0.001 * len(data)))
#     lat_lon_pairs = list(zip(list(sample_df.Start_Lat), list(sample_df.Start_Lng)))
#     map = folium.Map(width=300,height=500)
#     HeatMap(lat_lon_pairs).add_to(map)
#     #map
#     folium_static(map)

# with col2:
#     #plotting the marker points on US map with sample size of 0.1% of wholw dataset
#     sample_df_2 =data.sample(int(0.001 * len(data))) #creating a sample of 0.01%

#     #creating a variable containing the list of latitudes and longitudes
#     locations = sample_df_2[['Start_Lat', 'Start_Lng']]
#     locationlist = locations.values.tolist()
#     len(locationlist)
#     #locationlist[0]

#     #plotting the markers on the US map using folium library
#     map = folium.Map(width=300,height=500,zoom_start=12)
#     for point in range(0, len(locationlist)):
#         folium.Marker(locationlist[point]).add_to(map)
#     folium_static(map)






# #timezone = pd.DataFrame(data.Timezone.value_counts()).reset_index().rename(columns={"index":"Timezone","Timezone":"Cases"})
# fig9, ax9 = plt.subplots(figsize=(16,8))
# sns.histplot(data['Start_Time'].dt.hour, bins = 24)

# plt.xlabel("Start Time")
# plt.ylabel("Number of Occurence")
# plt.title('Accidents Count By Time of Day')

# show_graph9 = st.checkbox('Show Graph', value=True,key="9")

# if show_graph9:
#     st.pyplot(fig9)


#st.write(
#timezone = pd.DataFrame(data.Timezone.value_counts()).reset_index().rename(columns={"index":"Timezone","Timezone":"Cases"})
# def countPlot():
#     fig = plt.figure(figsize=(10, 4))
#     sns.countplot(x = "year", data = timezone)
#     st.pyplot(fig)
# countPlot()


# plt.figure(figsize=(9,4))
# plt.title('\n Accident cases for different timezones in US (2020)\n', size=20, color='grey')
# plt.xlabel('\n Timezone \n', fontsize=15, color='grey')
# plt.ylabel('\nAccident Cases\n', fontsize=15, color='grey')
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=12)
# a = sns.barplot(x=timezone.Timezone , y=timezone.Cases,palette="rainbow")
# import matplotlib.ticker as ticker
# a.yaxis.set_major_formatter(ticker.EngFormatter())
# show_graph9 = st.checkbox('Show Graph', value=True,key="9")

# if show_graph9:
#     st.pyplot(a)





# st.write(
# '''
# ##### Refrences:
# 1. Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. “A Countrywide Traffic Accident Dataset.”, 2019.

# 2. Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, Radu Teodorescu, and Rajiv Ramnath. "Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights." In proceedings of the 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems, ACM, 2019

# '''
# )

