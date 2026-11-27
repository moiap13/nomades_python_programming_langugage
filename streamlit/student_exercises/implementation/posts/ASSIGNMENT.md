# Blog Post Analysis Dashboard - Assignment

## Objective

Build a multi-page Streamlit application to analyze blog posts from multiple authors. The app will include data visualization, filtering capabilities, and interactive charts.

---

## Data Setup

You will find a CSV file named `users.csv` containing the following columns:
- `firstname`: **str**: First name of the author
- `lastname`: **str**: Last name of the author

In class we've generated a dataset of blog posts (using the `generate_csv.py` script) made by the authors in `users.csv`. The dataset is saved as `posts.csv` and contains the following columns:
- `title`: **str**: Title of the blog post
- `body`: **str**: Content of the blog post
- `created_at`: **str**: Creation date of the post in `YYYY-MM-DD` format
- `author`: **str**: Name of the author

---

## Main App Structure

Your final application should have the following structure:
```
project/
├── app.py              # Home page
├── ASSIGNMENT.md       # This assignment file
├── generate_csv.py     # Data generation script
├── posts.csv           # Generated post data
├── users.csv           # Author data
└── pages/
    ├── authors.py      # Author analysis page
    └── posts.py        # Post analysis page
```

---

## Step 2: Create the Home Page

Create `app.py` as the entry point of your Streamlit application.

**Requirements:**
- Set page configuration with a descriptive title and wide layout
- Display a welcome title
- Add page links to the Authors analysis and Post analysis pages using `st.page_link()`

---

## Step 3: Create the Authors Analysis Page

Create `pages/authors.py` for analyzing author statistics.

**Requirements:**

1. **Data Loading:**
   - Load data from `posts.csv`
   - Convert `created_at` column to datetime date format

2. **Sidebar Filters:**
   - Add a multiselect widget to filter by author names
   - The widget should show all unique authors from the dataset

3. **Display:**
   - Show the filtered DataFrame using `st.dataframe()`
   - Display the shape (row count) of the filtered data

4. **Visualization:**
   - Create a pie chart showing the distribution of posts per author
   - Use `plotly.express.pie()` for the visualization

**Key concepts:**
- `st.multiselect()` for selecting multiple options
- `df.groupby().size()` to count posts per author
- `px.pie()` to create pie charts

---

## Step 4: Create the Posts Analysis Page

Create `pages/posts.py` for analyzing post statistics.

**Requirements:**

1. **Data Loading:**
   - Load data from `posts.csv`
   - Convert `created_at` column to datetime date format

2. **Sidebar Filters:**
   - Add a date range selector using `st.date_input()`
   - Add a multiselect for author filtering (sorted alphabetically)
   - Add a text input for keyword search in post body

3. **Filtering Logic:**
   - Filter by date range using `between()`
   - Filter by selected authors using `isin()`
   - Filter by keyword presence in the body (case-sensitive search)

4. **Display:**
   - Show the filtered DataFrame

5. **Visualizations:**
   - **Bar Chart 1:** Number of posts per date (simple bar chart)
   - **Bar Chart 2:** Stacked bar chart showing posts per author per date (color-coded by author)

**Key concepts:**
- `st.date_input()` for date range selection
- `st.text_input()` for keyword search
- `px.bar()` for creating bar charts
- Grouping by multiple columns (`["created_at", "author"]`)
- Using `get_level_values()` to extract grouped data for axes

---

## Bonus Challenges

1. Add error handling for empty filter results
2. Add a download button to export filtered data as CSV
3. Add more visualizations (e.g., word count distribution, author activity timeline)

---

## Running Your App

To run the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

---

## Demo (for reference)

You have access to a Docker image demonstrating the expected result. To run it, you need to come to this folder from your host (`Windows`, `Mac` or `Linux`) and run:

```bash
docker compose up
```

Then open http://localhost:8501 in your browser to see the example application.

---

## External links
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Express Documentation](https://plotly.com/python/plotly-express/)
