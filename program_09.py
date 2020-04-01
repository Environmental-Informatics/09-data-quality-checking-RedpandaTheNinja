# add your header here
# Kevin Lee 
#Assignment 09 - Automated Data Quality Checking with Python
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    #replace -999 to np.NAN 
    DataDF = DataDF.replace(-999.0 , np.NaN)
    #located what we want to find and add it to the final results 
    ReplacedValuesDF.loc["1. No Data", :] = DataDF.isna().sum()
    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    #search the value and replace just like before   0 ≤ P ≤ 25; -25≤ T ≤ 35, 0 ≤ WS ≤ 10.
    #replace it with NaN values 
    DataDF['Precip'][ (DataDF['Precip'] < 0) | (DataDF['Precip'] > 25) ] = np.NaN
    DataDF['Max Temp'][ (DataDF['Max Temp'] < -25) | (DataDF['Max Temp'] > 35) ] =np.NaN
    DataDF['Min Temp'][ (DataDF['Min Temp'] < -25) | (DataDF['Min Temp'] > 35) ] =np.NaN
    DataDF['Wind Speed'][ (DataDF['Wind Speed']< 0) | (DataDF['Wind Speed'] > 10)] = np.NaN
    ReplacedValuesDF.loc["2. Gross Error", :] = DataDF.isna().sum() - ReplacedValuesDF.sum()
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    #Count total incidents for Max temp < min temp
    counter = len(DataDF.loc[DataDF['Max Temp'] < DataDF['Min Temp']])
    #Switch the values for Max temp < min Temp 
    DataDF.loc[ (DataDF['Max Temp']) < DataDF['Min Temp'] , ['Max Temp', 'Min Temp'] ] = DataDF.loc[ DataDF['Max Temp'] < DataDF[ 'Min Temp'], ['Min Temp', 'Max Temp']].values
    ReplacedValuesDF.loc["3. Swapped" , :] = [ 0 , counter , counter , 0 ]
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    #compute count on all the Max temp - min temp  is greater than 25 degrees 
    counter = len(DataDF.loc[ (DataDF['Max Temp'] - DataDF['Min Temp']) > 25])
    #replace NaN values for outliers 
    DataDF.loc[ (DataDF['Max Temp'] - DataDF['Min Temp']) > 25, ['Max Temp', 'Min Temp'] ] = np.NaN
    ReplacedValuesDF.loc["4. Range Fail" , :] = [ 0 , counter , counter , 0 ]
    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)



    import matplotlib.pyplot as plt

    #read the initial file again to compare, RawData  
    fileName = "DataQualityChecking.txt"
    RawData, RawReplacedValuesDF = ReadData(fileName)

    #Precip plot
    fig, a1 = plt.subplots(figsize=(10,10))
    a1.scatter(x = DataDF.index.values, y = RawData['Precip'], color = 'b', label = "raw data")
    a1.scatter(x = DataDF.index.values, y = DataDF['Precip'], color = 'r', label = "Processed data")
    a1.set(xlabel="Date",
       ylabel="Precipitation in mm",
       title="Precipitation" )
    plt.legend()
    plt.show()
    plt.close()

    #Max temp plot
    fig, a2 = plt.subplots(figsize=(10,10))
    a2.scatter(x = DataDF.index.values, y = RawData['Max Temp'], color = 'b', label = "raw data")
    a2.scatter(x = DataDF.index.values, y = DataDF['Max Temp'], color = 'r', label = "Processed data")
    a2.set(xlabel="Date",
       ylabel="Max Temp in C",
       title="Max Temp" )
    plt.legend()
    plt.show()
    plt.close()

    #Min temp plot
    fig, a3 = plt.subplots(figsize=(10,10))
    a3.scatter(x = DataDF.index.values, y = RawData['Min Temp'], color = 'b', label = "raw data")
    a3.scatter(x = DataDF.index.values, y = DataDF['Min Temp'], color = 'r', label = "Processed data")
    a3.set(xlabel="Date",
       ylabel="Min Temp in C",
       title="Min Temp" )
    plt.legend()
    plt.show()
    plt.close()
    
    #Wind Speed plot
    fig, a4 = plt.subplots(figsize=(10,10))
    a4.scatter(x = DataDF.index.values, y = RawData['Wind Speed'], color = 'b', label = "raw data")
    a4.scatter(x = DataDF.index.values, y = DataDF['Wind Speed'], color = 'r', label = "Processed data")
    a4.set(xlabel="Date",
       ylabel="Wind Speed in m/s",
       title="Wind Speed" )
    plt.legend()
    plt.show()
    plt.close()

#Save processed data into file format with replaced data
    DataDF.to_csv("ProcessedData.txt", sep='\t')
    ReplacedValuesDF.to_csv("ReplacedValues.txt", sep= '\t')