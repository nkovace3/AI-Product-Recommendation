import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import os
from django.conf import settings

base_dir = settings.BASE_DIR
subcategories_path = os.path.join(base_dir, 'Online_Retail_Categorized _1_.csv')
grocery_sells_path = os.path.join(base_dir, 'grocery_sells.csv')

# Getting the data

# subcategories = pd.read_csv('Online_Retail_Categorized _1_.csv')
subcategories = pd.read_csv(subcategories_path)


# Create a dictionary to store subcategories and their corresponding descriptions
subcategory_dict = {}

# Iterate through each row in the DataFrame
for index, row in subcategories.iterrows():
    subcategory = row['Subcategory']
    description = row['Description']

    # Check if the subcategory is already in the dictionary
    if subcategory in subcategory_dict:
        subcategory_dict[subcategory].append(description)
    else:
        # If not, create a new entry with the subcategory and a list containing the description
        subcategory_dict[subcategory] = [description]

# Load your data
# data = pd.read_csv('grocery_sells.csv')
data = pd.read_csv(grocery_sells_path)
unique_customer_names = data['Customer Name'].drop_duplicates().tolist()


# Encode categorical columns
label_encoders = {}
for column in ['Customer Name', 'Category', 'Sub Category']:
    le = LabelEncoder()
    data[column + '_encoded'] = le.fit_transform(data[column])
    label_encoders[column] = le

# Create user and item indices
user_ids = data['Customer Name_encoded'].unique()
item_ids = data['Sub Category_encoded'].unique()

user_id_map = {user_id: idx for idx, user_id in enumerate(user_ids)}
item_id_map = {item_id: idx for idx, item_id in enumerate(item_ids)}

# Map user and item IDs to numerical indices
data['user_idx'] = data['Customer Name_encoded'].map(user_id_map)
data['item_idx'] = data['Sub Category_encoded'].map(item_id_map)

# Get the number of users and items
num_users = data['user_idx'].nunique()
num_items = data['item_idx'].nunique()

# Hyperparameters
embedding_dim = 50

# Create a new DataFrame to store user-item interaction counts
interaction_counts = data.groupby(['user_idx', 'item_idx']).size().reset_index(name='interaction_count')


# Build and compile the model
class MatrixFactorizationModel(tf.keras.Model):
    def __init__(self, num_users, num_items, embedding_dim):
        super(MatrixFactorizationModel, self).__init__()
        self.user_embedding = tf.keras.layers.Embedding(num_users, embedding_dim)
        self.item_embedding = tf.keras.layers.Embedding(num_items, embedding_dim)
        self.user_bias = tf.keras.layers.Embedding(num_users, 1)
        self.item_bias = tf.keras.layers.Embedding(num_items, 1)
        self.dot = tf.keras.layers.Dot(axes=1)

    def call(self, inputs):
        user_embedding = self.user_embedding(inputs[:, 0])
        item_embedding = self.item_embedding(inputs[:, 1])
        user_bias = self.user_bias(inputs[:, 0])
        item_bias = self.item_bias(inputs[:, 1])
        dot_product = self.dot([user_embedding, item_embedding])
        output = dot_product + user_bias + item_bias
        return output


model = MatrixFactorizationModel(num_users, num_items, embedding_dim)
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Train the model with training data, using interaction count as sample weight
model.fit(
    x=interaction_counts[['user_idx', 'item_idx']].values,
    y=np.ones_like(interaction_counts['user_idx']),
    epochs=10,
    batch_size=10,
    sample_weight=interaction_counts['interaction_count'].values,
    validation_split=0.1
)


# Generate recommendations for a specific customer based on their purchase frequency
def generate_recommendations(customer_name, num_recommendations=10):
    # Get the user index for the given customer name
    user_idx = user_id_map[label_encoders['Customer Name'].transform([customer_name])[0]]

    # Get the items purchased by the user, sorted by purchase frequency
    user_purchases = interaction_counts[interaction_counts['user_idx'] == user_idx].sort_values(by='interaction_count',
                                                                                                ascending=False)

    if user_purchases.empty:
        print(f"No purchase history available for {customer_name}")
        return []

    # Choose the top N recommended items based on purchase frequency
    top_recommendations = user_purchases.head(num_recommendations)['item_idx'].values

    # Choose a random description from each recommended subcategory
    recommendations = []
    for item_idx in top_recommendations:
        subcategory = data[data['item_idx'] == item_idx]['Sub Category'].values[0]
        descriptions = subcategory_dict.get(subcategory, [])
        if descriptions:
            random_description = np.random.choice(descriptions)
            recommendations.append(random_description)

    return recommendations

def get_recommendations(customer_name_to_recommend):
    recommendations = generate_recommendations(customer_name_to_recommend, 10)
    return recommendations

def get_all(product):
    all_recs = {}
    for customer in unique_customer_names:
        recommendations = generate_recommendations(customer, 10)
        for rec in recommendations:
            if rec not in all_recs:
                all_recs[rec] = [customer]
            else:
                all_recs[rec].append(customer)

    if product in all_recs:
        return all_recs[product]
    else:
        noProductFound = f"No recommendations found for product: {product}"
        return [noProductFound]
