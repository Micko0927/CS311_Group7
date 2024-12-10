import sys
import pandas as PD
import numpy as NP
from scipy import stats
import matplotlib.pyplot as PLT

csv_files = {
    '2010': '2010.csv',
    '2015': '2015.csv',
    '2020': '2020.csv'
}

# Main Menu
def mainMenu(csv_files):
    year_options = {
        '1': '2010',
        '2': '2015',
        '3': '2020'
    }
    
    while True:
        print("\n------------------------------------------")
        print("       BAGUIO CITY POPULATION ANALYSIS    ")
        print("------------------------------------------")
        print("\nSelect the Option you want to explore:\n")
        print("1. 2010")
        print("2. 2015")
        print("3. 2020")
        print("4. Show Growth Percentage between Census")
        print("5. Predict 2025 Population")
        print("6. Exit Program\n")

        option = input("Enter your choice: ")

        if option == '4':
            print("\nGROWTH PERCENTAGE PER CENSUS:")
            displayGrowthPercentage()

        elif option == '5':
            print("\n2025 POPULATION PREDICTION:")
            predictPopulation2025()

        elif option == '6':
            print("\nProgram will now Exit...")
            sys.exit(0)
        
        elif option in year_options:
            year = year_options[option]
            csv_file = csv_files[year]
            df = PD.read_csv(csv_file)  # Load the CSV file into a DataFrame
            if optionSelection(df, year):
                continue  # If option 6 is chosen in option_selection, go back to main_menu
            else:
                break  # Exit the loop if the user chooses a year and proceeds to option_selection
        
        else:
            print("Please choose a valid option from the menu.\n")

    """
    This function calculates the population growth percentage between the years 2010, 2015, and 2020.
    It reads population data from a CSV file, extracts the total population for each year, and calculates
    the growth rate between 2010-2015, 2015-2020, and 2010-2020. It then prints the results.

    Steps:
        1. Load the CSV data using pandas.
        2. Extract the total population for 2010, 2015, and 2020.
        3. Calculate the growth percentage for each year range.
        4. Print the results.
    
    Returns:
        None
    """
def displayGrowthPercentage():
    df_total = PD.read_csv('total.csv')
    
    # Extract the total population data for the last row
    total_2010 = df_total.iloc[-1]['Population 2010 Census']
    total_2015 = df_total.iloc[-1]['Population 2015 Census']
    total_2020 = df_total.iloc[-1]['Population 2020 Census']
    
    # Formula to calculate growth percent
    growth_2010_to_2015 = ((total_2015 - total_2010) / total_2010) * 100
    growth_2015_to_2020 = ((total_2020 - total_2015) / total_2015) * 100
    growth_2010_to_2020 = ((total_2020 - total_2010) / total_2010) * 100
    
    print(f"2010 Total Population: {total_2010}")
    print(f"2015 Total Population: {total_2015}")
    print(f"2020 Total Population: {total_2020}\n")
    
    print(f"Growth from 2010 to 2015: {growth_2010_to_2015:.2f}%")
    print(f"Growth from 2015 to 2020: {growth_2015_to_2020:.2f}%")
    print(f"Growth from 2010 to 2020: {growth_2010_to_2020:.2f}%\n")

# This function will predict the 2025 Population
def predictPopulation2025():
    df_total = PD.read_csv('total.csv')
    
    total_2010 = df_total.iloc[-1]['Population 2010 Census']
    total_2015 = df_total.iloc[-1]['Population 2015 Census']
    total_2020 = df_total.iloc[-1]['Population 2020 Census']
    
    # Create arrays for the years and populations for fitting the model
    years = NP.array([2010, 2015, 2020])
    populations = NP.array([total_2010, total_2015, total_2020])
    
    # Fit a linear model
    coefficients = NP.polyfit(years, populations, 1)  # 1 means linear
    poly = NP.poly1d(coefficients)
    
    # Use the model to predict the population in 2025
    predicted_population_2025 = poly(2025)

    growth_2020_to_2025 = (
        (predicted_population_2025 - total_2020) / total_2020
    ) * 100
    
    print(f"Predicted Population in 2025: {predicted_population_2025:.0f}")
    print(f"Growth from 2020 to 2025 Predicted Population: "
          f"{growth_2020_to_2025:.2f}%\n")

# This function will display the mean, median, and mode of the selected year census
def displayDataSummary(dataframe, year):
    df_population = dataframe['Population']
    mean = NP.mean(df_population)
    median = NP.median(df_population)
    mode = stats.mode(df_population)
    
    print(f"Mean of Year {year}: {mean}")
    print(f"Median of Year {year}: {median}")
    print(f"Mode of Year {year}: {mode.mode[0]}")

# This function displays a pie chart showing the population distribution across
# the top 30 barangays and combines all others into 'Other Barangays'
def displayPopulationPieChart(dataframe, year):
    dataframe = dataframe.sort_values(by='Population', ascending=False)
    top_n = 30  
    other = dataframe[top_n:].sum()['Population']
    names = list(dataframe['Name'][:top_n]) + ['Other Barangays'] 
    populations = list(dataframe['Population'][:top_n]) + [other]

    PLT.figure(figsize=(12, 10))
    PLT.pie(populations, labels=names, autopct='%1.1f%%', startangle=140)

    PLT.title(f"Population Distribution of Baguio's Top {top_n} Barangays and "
              f"Other Barangays in the Year {year} Census")
    PLT.axis('equal')
    PLT.show()

# This function will display a Bar Graph of the Top 5 highest populations of the
# chosen year census.
def displayTop5BarGraph(dataframe, year):
    top_5 = dataframe.sort_values(by='Population', ascending=False).head(5)
    
    PLT.figure(figsize=(10, 6))
    PLT.barh(top_5['Name'], top_5['Population'], color='blue')
    PLT.xlabel('Population')
    PLT.ylabel('Barangay')
    PLT.title(f'Top 5 Barangays with Highest Population in {year} Census')
    PLT.gca().invert_yaxis()
    PLT.show()

# This function will display a Bar Graph of the Top 5 lowest populations of the
# chosen year census.
def displayBottom5BarGraph(dataframe, year):
    bottom_5 = dataframe.sort_values(by='Population', ascending=True).head(5)
    
    PLT.figure(figsize=(10, 6))
    PLT.barh(bottom_5['Name'], bottom_5['Population'], color='red')
    PLT.xlabel('Population')
    PLT.ylabel('Barangay')
    PLT.title(f'Top 5 Barangays with Lowest Population in {year} Census')
    PLT.gca().invert_yaxis()
    PLT.show()

# Option Selection per Year
def optionSelection(df, year):
    while True:
        print("\n-------------------------")
        print(f"       {year} CENSUS       ")
        print("-------------------------\n")
        print("Select the Option you want to explore:\n")
        print("1. View Data Content")
        print("2. View Data Summary")
        print("3. Display Top 30 Population Pie Chart")
        print("4. Top 5 Highest Population per Barangay")
        print("5. Top 5 Lowest Population per Barangay")
        print("6. Go Back to Main Menu\n")
    
        option = input("Enter your choice: ")

        if option == '1':
            print(f"\nData Content of Year {year} Census:\n")
            print(df)

        elif option == '2':
            print(f"\nData Summary of Year {year} Census:\n")
            displayDataSummary(df, year)

        elif option == '3':
            print(f"\nDisplaying Population Pie Chart:\n")
            displayPopulationPieChart(df, year)

        elif option == '4':
            print(f"\nDisplaying Top 5 Highest Population Bar Graph:\n")
            displayTop5BarGraph(df, year)

        elif option == '5':
            print(f"\nDisplaying Top 5 Lowest Population Bar Graph:\n")
            displayBottom5BarGraph(df, year)

        elif option == '6':
            return True  # Option to go back to Main Menu
        
        else:
            print("Please choose a valid number.")

# Main Menu
mainMenu(csv_files)
