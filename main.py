import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df=pd.read_excel('product.xlsx')


print(df.info())
print(df.describe())
print(df.head(10))
print(df.tail(10))

pt=df.fillna(0)

#1. Determine the most common product categories.

category = pt.groupby('Category').size()     
category_dict=category.to_dict()    #make it dictonary
max_key = max(category_dict, key=category_dict.get)  #Find key of maximum Product
max_value = category_dict[max_key]      #Value of that Product
print("Most common Product:", max_key)
print("Count:", max_value)

#2. Analyze most rated products using histograms and boxplots.

#Histogram
figsize=(10, 5)
a=sns.histplot(pt['Product_Rating'], bins=20, color='red') #Make the histogram
for i in a.patches:                   #for showing value in each bar
    height = i.get_height()
    plt.text(i.get_x()+i.get_width()/2, height+5,int(height), ha='center',fontsize=9)
plt.title("Distribution of Product Ratings")
plt.xlabel("Product Rating")
plt.ylabel("Frequency")
plt.show()

#Boxlpot
figsize=(8, 4)
sns.boxplot(x=pt['Product_Rating'], color='blue')
plt.title("Boxplot of Product Ratings")
plt.xlabel("Product Rating")
plt.show()


#3.Explore correlation between price, Product ratings and Average Rating of Similar Products

data=pd.DataFrame({'Price': pt['Price'], 'Producr_Rating': pt['Product_Rating'],'Average_Rating': pt['Average_Rating_of_Similar_Products']})
cor = data.corr()  #calculate correlation
plt.figure(figsize=(8, 6))
sns.heatmap(cor, annot=True, fmt=".2f",  linewidth=0.5)
plt.title("Correlation")
plt.show()


#4.Compare Product_id vs Average Rating of Similar Products to identify which sellers attract the most engagement  using bar and line plots.

#Barplot
seller=pt.groupby('Product_ID')['Average_Rating_of_Similar_Products'].mean().sort_values(ascending=False)
top_sellers = seller.head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_sellers.index, y=top_sellers.values, color="green")
plt.title("Top Sellers by Avg Rating of Similar Products")
plt.xlabel("Seller ID")
plt.ylabel("Average Rating of Similar Products")
plt.show()

#lineplot
plt.figure(figsize=(12, 6))
sns.lineplot(x=top_sellers.index, y=top_sellers.values, marker='o', color='green')
plt.xticks(rotation=45)
plt.title("Trend: Avg Rating of Similar Products per Seller")
plt.xlabel("Seller ID")
plt.ylabel("Average Rating of Similar Products")
plt.tight_layout()
plt.show()



#5. Visualize price trends using scatter plots and line charts.

#Scatter Plot
plt.figure(figsize=(10, 6))
a1=pt['Product_Rating'].head(1000)
a2=pt['Price'].head(1000)
sns.scatterplot(data=pt, x=a1, y=a2, hue='Category', alpha=0.7)
plt.title("Product Rating vs Price")
plt.xlabel("Product Rating")
plt.ylabel("Price")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Line chart
avg_price_by_category = pt.groupby('Category')['Price'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=avg_price_by_category, x='Category', y='Price', marker='o')
plt.title("Average Price per Category")
plt.xlabel("Category")
plt.ylabel("Average Price")
plt.tight_layout()
plt.show()


#6. Use pie chart to show category-wise product share and Generate bar charts to display 

cate = pt['Category'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(cate.values, labels=cate.index, autopct='%1.1f%%', startangle=140)
plt.title("Category-wise Product Share")
plt.tight_layout()
plt.show()

#7. Detect outliers in prices using IQR and boxplots.

#IQR Method
price =np.array(pt['Price'])
Q1 = np.percentile(price,25)
Q3 = np.percentile(price,75)
IQR =Q3-Q1
lower_bound= Q1-1.5*IQR
upper_bound= Q3+1.5*IQR
outlier= price[(price < lower_bound) | (price > upper_bound)]
print(outlier)

#Box Plot
figsize=(6,4)
plt.boxplot(pt['Price'],vert=False)
plt.xlabel("Price")
plt.title("Box plot for outlier Detection")
plt.show()

#8. Spot extreme or invalid rating values using Z-score technique.

arr=np.array(pt['Product_Rating'])
mean_i=arr.mean()
std_i=arr.std(ddof=1)
z_score_i=(arr-mean_i)/std_i
outlier=arr[np.abs(z_score_i)>3]
print(outlier)
