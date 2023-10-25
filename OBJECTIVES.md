# TODO

- [x] Rename `selectbox.py` to `form_fields.py` and `SelectBox` class to `FormField`.
- [x] Rename `options.py` to `form_options.py` and corresponding.
- [x] Rename `reader.py` to `schema_reader.py`.
- [x] Make a constant in `constants.py` as `DATA_SCHEMA_PATH = Path("src/database/schema.json")`.
- [x] Make constants for `LOCALITY_NAME.csv` and `CITY.csv` in `constants.py`.
- [x] Add `LUXURY_SCORE` feature into `schema.json`, streamlit form and everywhere.
- [x] How can you validate the `LOCALITY_NAME` belongs to the particular `CITY`?
- [x] How can you add new city dataset into the picture?
- [x] Store user's new data into different directory to differentiate between main data and user's data. And show analysis on it.
- [x] Use `functions` with `@st.cache` decorator to optimize the **Analytics Page**.
- [ ] Make a page to show Model Evaluation Metrics. Which are useful for other developers.
- [ ] ~~Add logging in the app.~~ **(Not for now.)**
- [x] Fetch the new discussed Gurgaon data and perform EDA on it. Then, use that data in the project for better analysis and prediction.
- [ ] Do something about Recommender system.

## Analytics Features

- [x] Add selectbox to select CITY and also refresh the map which recenter the map to the city.
- [x] Add BHK radio button in `scatter_mapbox` plot.
- [ ] Create new page and add better plots in new page.

# Features

- [x] ~~Use `st.tabs()` instead of `st.radio()` for good UI.~~
- [x] ~~Add a custom streamlit theme.~~
- [x] Enhance the radio buttons in the [page](./pages/1_Price_Prediction.py) or you can use `st.selectbox` instead.

- [x] Add summary for **Newly Added Data** by user in [Add New City Page](pages/2_Add_New_City.py)
  - [x] Insights about:
    - Shape of the Data
    - No. of property in each **CITY**
    - No. of property in each **PROPERTY_TYPE**
  - [x] ~~Show Distribution of data. _Plot graphs for this._ (in `st.expander`)~~
  - [x] Write that for more insights go to [Analytics Page](pages/3_Analytics_Page.py)

# Suggestions

### How does the data get in for model building?

1. Fetch data from database.
2. Clean data at step first to clean further for specific `PROPERTY_TYPE`.
3. Clean data at step second with every property entity class's method `PropertyType.clean_dataset()`.
4. Now we have 6 dataset in total to train models.
5. Now here raises a question that **how do I train models using these many dataset at once?**

### How to clean the raw data?

> **Things to Remember**
>
> - First do all the things with `gurgaon_10k.csv` dataset, then replicate the process for MongoDB.
> - Dump the cleaned data (only with step first cleaning) in the MongoDB and clean the data further with each property entity method `PropertyType.clean_dataset()` and train the model.
> - You need to take care of the CITY and LOCALITY_NAME options because they are fetched from a `.csv` file. You need to update them regularly when the user fetches new city data.

> **Questions & Doubts**
>
> 1. Should fetch data every time to show Analysis?
> 2. I have to save the trained model into a directory.
> 3. I have to create a button to fetch new city data.
> 4. I have to create a button to re-train the model on new dataset (which contains the data of the new city fetched by user.)
> 5. As you fetching, cleaning, training the model on the newly fetched data take a lot of time. How do I tackle this.

#### Step First

1. Select columns for model building and analytics.
2. Decode the encoded features like `FACING, FURNISH, FLOOR_NUM, FEATURES, FORMATTING_LANDMARK_DETAILS`, etc.
3. After cleaning at first step dump the data to MongoDB to process further.

### How to fetch data from website to dump in the database?

I added a form from where users can fetch the data of a particular CITY.

> **Make a `streamlit` secret string** from where I can disable this feature to avoid the request blocking.

Now I fetched data from website then I have to preprocess the data to dump it into the database. For that I have to **create two-step function** to clean the data for each `PROPERTY_TYPE`.

1. I need to clean the whole fetched dataset with the first function which ready the dataset to clean further for each `PROPERTY_TYPE`.
2. Now the cleaned datasets being cleaned further by the specific property entity's method `clean_data()`.

And then after cleaning the dataset we are ready to dump them into the database.

### Process of adding new CITY data to train the model on it.

1. User can choose whether they want to train a new model on their data or train a new model on new data and old data combined.
2. Display all the **CITY and No. of data point** which are already present in the dataset. Update it on daily basis by reading the dataset.
3. **DISCUSS**: If the user added a new CITY data then how do you add that city's `LOCALITY_NAME` and `CITY` into `form_options`.
