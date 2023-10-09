import pandas as pd
from tabulate import tabulate

# Your existing code...
df = pd.read_excel('/content/food_recipes.xlsx')  # Replace 'your_dataset.csv' with your file path
df = df.head(50)
columns_to_drop = ['url', 'record_health','vote_count','rating','description','author','tags','category','diet','course']
df.drop(columns=columns_to_drop, inplace=True)
columns_to_check = ['ingredients']
df.dropna(subset=columns_to_check, inplace=True)

# Group recipes by cuisine and concatenate the recipes within each group
df['prep_time'] = df['prep_time'].str.replace('M', '').astype(int)
df['cook_time'] = df['cook_time'].str.replace('M', '').astype(int)
df['Total Prep Time (Minutes)'] = df['prep_time'] + df['cook_time']
columns_to_drop = ['prep_time','cook_time']
df.drop(columns=columns_to_drop, inplace=True)

# Print all cuisines in a table
grouped = df.groupby('cuisine')
cuisine_table = []
for cuisine, group in grouped:
    cuisine_table.append([cuisine])
    # for index, row in group.iterrows():
    #     cuisine_table.append([row['recipe_title'], row['ingredients']])
    # cuisine_table.append([])

# Print the cuisine table
print(tabulate(cuisine_table, headers=['Cuisine'], tablefmt='pretty'))

# Ask user to enter a cuisine and display dishes in that cuisine
keyword = input('Enter the cuisine ')
search_cuisine = df[df['cuisine'].str.contains(keyword, case=False)]
search_cuisine = search_cuisine.copy()
time_frame = [0, 30, 60, float('inf')]  # Define your own time ranges as needed
labels = ['Short', 'Medium', 'Long']
search_cuisine['Prep Time Category'] = pd.cut(search_cuisine['Total Prep Time (Minutes)'], bins=time_frame, labels=labels)
final_df = search_cuisine.sort_values(by=['Prep Time Category','recipe_title'],ascending=[True,True])

# Print the final results
# print(final_df)

# Print the final results
print(tabulate(final_df, headers='keys', tablefmt='pretty'))

# Ask user to enter a dish and display its details
keyword = input('Enter the recipe ')
search_results = df[df['recipe_title'].str.contains(keyword, case=False)]

# Filter the DataFrame to include only recipes with at least one matching ingredient
user_ingredients = [ingredient.lower() for ingredient in input("Enter ingredients separated by spaces: ").split()]
df['Matched_Ingredients'] = df['ingredients'].apply(lambda x: sum(1 for ingredient in user_ingredients if ingredient.lower() in x.lower().split('|')))
filtered_df = df[df['Matched_Ingredients'] > 0]

# Print the list of matching recipe titles
matching_recipe_titles = filtered_df['recipe_title'].tolist()
if matching_recipe_titles:
    print("Matching Recipe Titles:")
    for title in matching_recipe_titles:
        print(title)
else:
    print("No matching recipes found.")
