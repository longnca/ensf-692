# calgary_dogs.py
# LONG NGUYEN
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd


def main():
    # Stage 1: DataFrame creation
    # Import data here
    df = pd.read_excel("CalgaryDogBreeds.xlsx")

    # # My personal EDA check
    # print(df.head())
    # print(df.info())
    # print("The unique values of Year: ", df['Year'].unique())
    # print("The unique values of Month: ", df['Month'].unique())
    # print("The unique values of Breed: ", df['Breed'].unique())
    # print("Number of unique values of Breed: ", df['Breed'].nunique())

    # Set and sort the multi-index for the DF
    # I chose the column 'Breed' as the primary index since it's easier for
    # data access and analysis in the next step.
    df.set_index(['Breed', 'Year', 'Month'], inplace=True)
    df.sort_index(inplace=True)

    # # Optional: check the DF after setting and sorting multi-index
    # print(df.head(10))

    print("\nENSF 692 Dogs of Calgary")

    # Stage 2: User input stage
    user_input = get_user_input(df)

    # Stage 3: Data analysis stage
    calculate_breed_stats(df, user_input)


def get_user_input(df):
    """
    Take the user input and accept all entries in uppercase, lowercase,
    camel case, and mixed case by converting them to uppercase.

    Parameter:
        df (pd.DataFrame): the DataFrame loaded by reading the Excel dataset.

    Return:
        str: The String input if the value is found in the 'Breed' index.
        If not found, raise a KeyError exception and continue the while loop.
    """
    while True:
        try:
            # Take the user input and convert it to uppercase.
            user_input = input("Please enter a dog breed: ").upper()
            # Check if the breed exists in the index
            if user_input in df.index.get_level_values('Breed'):
                return user_input
            else:
                raise KeyError
        except KeyError as e:
            print("Dog breed not found in the data. Please try again.")


def calculate_breed_stats(df, breed):
    """
    Calculate all the statistics that are required in Stage 3 (Data Analysis).

    Parameters:
        df (pd.DataFrame): the DataFrame loaded by reading the Excel dataset.
        breed (str): The dog breed taken from the user input.

    Return:
        None
    """
    # Use the IndexSlice object to slice the DF.
    idx = pd.IndexSlice

    # 3.1. Find all the years from the 'year' index of the breed input.
    # Extract the specific breed name.
    breed_data = df.loc[idx[breed, :, :]]
    # Find and combine all the years of the selected breed.
    breed_years = ", ".join(map(str, breed_data.index.get_level_values('Year').unique()))
    # Print the results.
    print(f"The {breed} was found in the top breeds for years: {breed_years}. ")

    # 3.2. Calculate the total number of registrations of the selected breed found.
    total_breed_all_years = breed_data['Total'].sum()
    print(f"There have been {total_breed_all_years} {breed} dogs registered total.")

    # 3.3. Calculate the percentage of selected breed registrations for each year.
    # Set the list of all expected years in the DataFrame
    years = [2021, 2022, 2023]
    for year in years:
        total_dogs_per_year = df.loc[idx[:, year, :], 'Total'].sum()
        selected_breed_per_year = df.loc[idx[breed, year, :], 'Total'].sum()
        percentage_breed_per_year = round((selected_breed_per_year / total_dogs_per_year) * 100, 6)
        print(f"The {breed} was {percentage_breed_per_year}% of top breeds in {year}.")

    # 3.4. Calculate the percentage of selected breed registrations across all years.
    total_dogs_all_years = df.loc[idx[:, years, :], 'Total'].sum()
    percentage_breed_all_years = round((total_breed_all_years / total_dogs_all_years) * 100, 6)
    print(f"The {breed} was {percentage_breed_all_years}% of top breeds across all years.")

    # 3.5. Find the months that were most popular for the selected breed.
    # Calculate the registrations grouped by Months.
    breed_months = breed_data.groupby('Month').count()
    # Sort the values by the 'Total' count of occurrences
    sorted_breed_months = breed_months.sort_values(by='Total', ascending=False)
    # print(sorted_breed_months)
    # Find the maximum count of occurrences
    max_occurrences = sorted_breed_months['Total'].max()
    # Filter the months that have more registrations than the average.
    popular_months = sorted_breed_months[sorted_breed_months['Total'] == max_occurrences].index.tolist()
    print(f"Most popular month(s) for {breed} dogs: {', '.join(popular_months)}")


if __name__ == '__main__':
    main()
