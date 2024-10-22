#!/usr/bin/env python
# coding: utf-8

# ### In this Project we will analyse the World Population in 2015 with data from the CIA World Factbook 
# 
# 
# In this project, we'll use SQL in Jupyter Notebook to explore and analyze data from this database.

# In[30]:


import matplotlib.pyplot as plt
import pandas as pd


# In[3]:


get_ipython().run_cell_magic('capture', '', '%load_ext sql\n%sql sqlite:///factbook.db \n\n#Connecting the Jupyter Notebook to the database\n')


# In[3]:


get_ipython().run_cell_magic('sql', '', "\nSELECT *\n  FROM sqlite_master\n WHERE type='table'; \n\n#Here we format the input as a table.\n")


# ### Data set: 
# 
# The dataset is quite simple and is composed of 11 colums and 262 row. 
# 
# - **id** - id number attribuated to a country.
# - **code** - country code, made from the two first letters of the country.
# - **area** - total area of the country (area_water + area_land).
# - **population** - population of the country 
# - **population_growth** - ratio of the population growth in 2015 
# - **birth_rate**
# - **death_rate**
# - **migration_rate** - ratio of people that left the country to another.
# 
# It is important to note that the last row (id 262) is not a country but "World" (code: xx). In the end the data is only composed of 261 countries. 
# 

# In[109]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM facts\nLIMIT 10;\n')


# ## Finding the maximum and minimum of population and population growth in all the countries?

# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(population) AS min_pop,\n       MAX(population) AS max_pop,\n       MIN(population_growth) AS min_pop_growth,\n       MAX(population_growth) AS max_pop_growth\nFROM facts;\n')


# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM facts\nWHERE population == (SELECT MIN(population)\n                     FROM facts);\n')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM facts\nWHERE population == (SELECT MAX(population)\n                     FROM facts);\n')


# ## Looking up the populaton details of resident country Ghana

# In[10]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM   facts\nWHERE  name == "Ghana";\n')


# ## Finding the outliers
# As stated in the explanation above, the row "World" is the total of the whole database (261 countries). It does appear as the "country" with the max population (7.2 billions) in our query and messes up our analysis. We need to write another query, leaving "World" out of it. Antitartica also appears with 0 population. There are outliers.

# In[4]:


#SQL CODE.
#Delete comments to run SQL without errors
get_ipython().run_line_magic('%sql', '')
SELECT MIN(population) AS min_pop,
       MAX(population) AS max_pop,
       MIN(population_growth) AS min_pop_growth,
       MAX(population_growth) AS max_pop_growth
FROM  facts
WHERE name NOT IN ('World','Antarctica'); 



# Taking World and Antarctica out,  we can see that there is a country with about 1.3 billion people and a country with a population of 48

# ## Finding Densely Populated Countries¶
# 
# To finish, I will build on the query above to find countries that are densely populated. I'll identify countries that have:
# 
# Above average values for population.
# Below average values for area.

# First Let us calculate the average population and average land area for the entire world.

# In[28]:


get_ipython().run_cell_magic('sql', '', "SELECT AVG(population) AS avg_population,\n       AVG(area) AS avg_area\nFROM facts\nWHERE name <>'Wolrd';\n")


# In[29]:


get_ipython().run_cell_magic('sql', '', 'SELECT name, population, area\nFROM facts\nWHERE population > (SELECT AVG(population)\n                    FROM facts\n                   )\nAND area <(SELECT AVG(area)\n          FROM facts\n          ) \nORDER BY 2 DESC;\n')


# ## VISUALIZATIONS
# 
# ### PLOTTING A HISTOGRAM SHOWING THE POPULATION DISTRIBUTION ACROSS COUNTRIES

# In[39]:


get_ipython().run_cell_magic('sql', 'result <<', "SELECT population \nFROM facts \nWHERE name NOT IN ('World', 'Antarctica');\n")


# In[40]:


#Python Code for Visualization
df = result.DataFrame()

plt.figure(figsize=(10, 6))
plt.hist(df['population'], bins=30, edgecolor='k')
plt.title('Population Distribution')
plt.xlabel('Population')
plt.ylabel('Number of Countries')
plt.show()


# ### PLOTTING A SCATTER PLOT BETWEEN POPULATION AND POPULATION GROWTH TO SHOW THE RELATIONSHIP

# In[42]:


get_ipython().run_cell_magic('sql', 'result1 <<', "SELECT population, population_growth\nFROM facts\nWHERE name NOT IN ('World','Antarctica');\n")


# In[45]:


df = result1.DataFrame()

plt.figure(figsize=(10,6))
plt.scatter(df['population'], df['population_growth'], alpha=0.4)
plt.title('Population vs Population Growth')
plt.xlabel('Population')
plt.ylabel('Population Growth %')
plt.show()


# ### PLOTTING A BAR CHART TO SHOW THE TOP 10 MOST POPULOUS COUNTRIES

# In[50]:


get_ipython().run_cell_magic('sql', 'result2 <<', "SELECT name, population\nFROM facts\nWHERE name NOT IN ('World', 'Antarctica')\nORDER BY population DESC\nLIMIT 10;\n")


# In[51]:


df = result2.DataFrame()

# Plot bar chart
plt.figure(figsize=(12, 6))
plt.bar(df['name'], df['population'], color='skyblue')
plt.title('Top 10 Most Populous Countries')
plt.xlabel('Country')
plt.ylabel('Population')
plt.xticks(rotation=90)
plt.show()


# ### PLOTTING A BAR CHART TO SHOW THE LEAST 10 MOST POPULOUS COUNTRIES

# In[71]:


get_ipython().run_cell_magic('sql', 'result3 <<', "SELECT name, population\nFROM facts\nWHERE name NOT IN ('World', 'Antarctica')\nAND population IS NOT NULL\nORDER BY population ASC\nLIMIT 10;\n")


# In[62]:


#Finding the number of entries with None for population.One way to go around this is to clean and standardize the data by either droping the entries with none or replacing with the mean.
print(df['population'].isnull().sum())


# In[73]:


df = result3.DataFrame()

# Plot bar chart
plt.figure(figsize=(10, 6))
plt.bar(df['name'], df['population'], color='skyblue')
plt.title('Least 10 Most Populous Countries')
plt.xlabel('Country')
plt.ylabel('Population')
plt.xticks(rotation=45)
plt.show()


# ### PLOTTING BOXPLOTS TO SHOW THE DISTRIBUTION OF POPULATION GROWTH RATES ACROSS COUNTRIES WHOSE POPULATION IS HIGHER THAN THE AVERAGE

# In[81]:


get_ipython().run_cell_magic('sql', 'result4 <<', "SELECT name, population_growth\nFROM facts\nWHERE population > (SELECT AVG(population)\n                    FROM facts\n                   ) \nAND name NOT IN ('World','Antarctica');\n")


# In[86]:


df = result4.DataFrame()

# Plot box plot
plt.figure(figsize=(20, 10))
df.boxplot(column='population_growth', by='name', grid=True, rot=45, fontsize=10)
plt.title('Population Growth Rate by Country')
plt.suptitle('')
plt.xlabel('Country')
plt.ylabel('Population Growth (%)')
plt.show()


# ### PLOTTING A PIE CHART TO SHOW THE WEIGHTS OF MIGRATION RATE, BIRTH RATE AND DEATH RATE ON THE POPULATION GROWTH OF SELECTED COUNTRIES.

# In[95]:


get_ipython().run_cell_magic('sql', 'result5 <<', "SELECT migration_rate, birth_rate, death_rate\nFROM facts\nWHERE name == 'Belgium';\n")


# In[105]:


df = result5.DataFrame()

migration_rate = df['migration_rate'].values[0]
birth_rate = df['birth_rate'].values[0]
death_rate = df['death_rate'].values[0]

labels = ['migration_rate','birth_rate','death_rate']
colors = ['#ff9999','#66b3ff','#99ff99']
weights = [migration_rate,birth_rate,death_rate]

plt.figure(figsize=(10,6))
plt.pie(weights, autopct='%1.2f%%', startangle=140, colors=colors, textprops={'fontsize': 14},labeldistance=1.05)
plt.title('Weights of Migration Rate, Birth Rate, and Death Rate on Population Growth of Belgium')
plt.show()


# ### PLOTTING A PIE CHART TO SHOW THE WEIGHTS OF MIGRATION RATE, BIRTH RATE AND DEATH RATE ON THE POPULATION GROWTH OF SELECTED COUNTRIES.

# In[106]:


get_ipython().run_cell_magic('sql', 'result6 <<', "SELECT migration_rate, birth_rate, death_rate\nFROM facts\nWHERE name == 'Ghana';\n")


# In[108]:


df = result6.DataFrame()

migration_rate = df['migration_rate'].values[0]
birth_rate = df['birth_rate'].values[0]
death_rate = df['death_rate'].values[0]

labels = ['migration_rate','birth_rate','death_rate']
colors = ['#ff9999','#66b3ff','#99ff99']
weights = [migration_rate,birth_rate,death_rate]

plt.figure(figsize=(10,6))
plt.pie(weights, autopct='%1.2f%%', startangle=140, colors=colors, textprops={'fontsize': 14},labeldistance=1.05)
plt.title('Weights of Migration Rate, Birth Rate, and Death Rate on Population Growth of Ghana')
plt.show()


# In[ ]:




