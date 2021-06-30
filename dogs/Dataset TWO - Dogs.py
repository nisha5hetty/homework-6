#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[292]:


import pandas as pd
import openpyxl


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[293]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx")


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[294]:


df.shape


# In[295]:


df.dtypes


# In[296]:


df.columns = df.columns.str.replace(' ', '')


# In[297]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[298]:


df.head()


# Each row is a licensed dog. SpayedorNeut is whether the dog has been spayed or neutered. Vaccinated is whether the dog has been vaccinated.

# In[ ]:





# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# 1. How many male trained dogs are there vs female trained dogs?
# 2. Which dog is the youngest and oldest?
# 3. How many unvaccinated dogs are there?
# 4. How many huskies are there (primary or secondary breed)?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[299]:


df.PrimaryBreed.value_counts().head(10)


# In[300]:


df.PrimaryBreed.value_counts().head(10).sort_values(ascending=True).plot(kind='barh')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[301]:


df[df.PrimaryBreed != 'Unknown'].PrimaryBreed.value_counts().head(10)


# ## What are the most popular dog names?

# In[302]:


df.AnimalName.value_counts().head()


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[303]:


df[df.AnimalName=='Nisha']


# In[304]:


len(df[df.AnimalName=='Max'])


# In[305]:


len(df[df.AnimalName=='Maxwell'])


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[306]:


(df.GuardorTrained.value_counts(normalize=True) * 100).round(2)


# ## What are the actual numbers?

# In[216]:


df.GuardorTrained.value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[307]:


df.GuardorTrained.value_counts


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[218]:


df.GuardorTrained.fillna("No", inplace=True)


# In[308]:


df.GuardorTrained.value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[309]:


df[(df.PrimaryBreed != 'Unknown') & (df.GuardorTrained=='Yes')].PrimaryBreed.value_counts().head()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[310]:


df['Year'] = df['AnimalBirth'].apply(lambda birth: birth.year)


# In[311]:


df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[337]:


df['Age'] = 2021 - df.Year


# In[338]:


df.head()


# In[341]:


df.Age.mean().round()


# # Joining data together

# In[ ]:





# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[312]:


df_nbhd = pd.read_csv("zipcodes-neighborhoods.csv")
df_nbhd


# In[313]:


df = df.merge(df_nbhd, left_on='OwnerZipCode', right_on='zip')


# In[314]:


df = df.drop(columns=['OwnerZipCode'])
df.head()


# In[315]:


df = df.rename(columns={
    'neighborhood': 'OwnerNeighborhood',
    'zip': 'OwnerZipCode',
    'borough': 'OwnerBorough'
})
df


# In[ ]:





# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[316]:


df[df.OwnerBorough=='Bronx'].AnimalName.value_counts().head()


# In[317]:


df[df.OwnerBorough=='Brooklyn'].AnimalName.value_counts().head()


# In[318]:


df[df.OwnerNeighborhood=='Upper East Side'].AnimalName.value_counts().head()


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[319]:


df.groupby('OwnerNeighborhood')['PrimaryBreed'].value_counts().sort_values(ascending=False)


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[320]:


df[(df.PrimaryBreed != 'Unknown') & (df.SpayedorNeut=='Yes')].AnimalGender.value_counts()


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[434]:


df['monochrome']


# In[435]:





# ## How many dogs are in each borough? Plot it in a graph.

# In[321]:


df.OwnerBorough.value_counts()


# In[322]:


df.OwnerBorough.value_counts().sort_values(ascending=True).plot(kind='barh', title='Dogs per borough')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[323]:


get_ipython().system('ls')


# In[324]:


df_bpop = pd.read_csv("boro_population.csv")
df_bpop


# In[325]:


df = df.merge(df_bpop, left_on='OwnerBorough', right_on='borough')


# In[326]:


df = df.drop(columns=['OwnerBorough'])
df.head()


# In[327]:


df = df.rename(columns={
    'borough': 'OwnerBorough',
    'population': 'BoroughPopulation',
    'area_sqmi': 'BoroughAreaSqMi'
})
df


# In[334]:


df.groupby('OwnerBorough')['BoroughPopulation'].value_counts().sort_values(ascending=False)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[425]:


df.groupby(by='OwnerBorough').PrimaryBreed.value_counts()


# In[422]:


df.groupby(by='OwnerBorough').PrimaryBreed.value_counts().nlargest(5)


# In[423]:


df.groupby(by='OwnerBorough').PrimaryBreed.value_counts().nlargest(5).to_frame(name='Counts')


# In[424]:


df.groupby(by='OwnerBorough').PrimaryBreed.value_counts().nlargest(5).to_frame(name='Counts').reset_index()


# In[428]:


df.groupby('OwnerBorough').PrimaryBreed.value_counts().groupby(level=0, group_keys=False).nlargest(5).to_frame(name='Counts').reset_index()


# In[431]:


df.groupby('OwnerBorough').PrimaryBreed.value_counts()     .groupby(level=0, group_keys=False)     .nlargest(5)     .plot(kind='barh', title='Top 5 breeds in each borough')


# In[ ]:





# ## What percentage of dogs are not guard dogs?

# In[275]:


(df.GuardorTrained.value_counts(normalize=True) * 100).round(2)

