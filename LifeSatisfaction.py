import pandas as pd


def readWEOFile():
    print("Reading \"WEO_Data.csv\"")

    #Read the File into the DataFrame
    worldData = pd.read_csv("WEO_Data.csv", sep="	", encoding="ISO-8859-1")
    #Dropping the Columns/Row that are useless
    worldData = worldData.drop(['Subject Descriptor', 'Units', 'Scale', 'Country/Series-specific Notes', 'Estimates Start After'], axis=1)
    worldData = worldData.drop(189)
    #Renaming the columns
    worldData = worldData.rename(columns={"Country": "Country (Full Name)", "2015": "Gross Domestic Product per Capita (USD)"})

    print(worldData.head(), "\n", "\n", worldData.tail(), "\n")

    return worldData

def importDataFiles():
    #Create the main DataFrame
    dataFrame = readWEOFile()
    print("Reading \"Life metrics.csv\"")

    #Reads the file in the DataFrame
    lifeSatisfaction = pd.read_csv("Life metrics.csv")

    #Dropping the Columns/Row that are useless
    lifeSatisfaction = lifeSatisfaction.drop(
        ['LOCATION', 'INDICATOR', 'Measure', 'MEASURE', 'INEQUALITY', 'Unit', 'PowerCode Code', 'PowerCode Code',
         'PowerCode', 'Reference Period Code', 'Reference Period', 'Flag Codes', 'Flags'], axis=1)

    print(lifeSatisfaction.head(), "\n")
    print(list(lifeSatisfaction.columns), "\n")

    print("Starting to Combine the two DataFrames")
    for ind in lifeSatisfaction.index:
        #The Column where the value will be stored
        header = str(lifeSatisfaction['Indicator'][ind]) + " - " + str(lifeSatisfaction['Inequality'][ind]) + " (" + str(lifeSatisfaction['Unit Code'][ind]) + ")"
        #The Value
        value = lifeSatisfaction['Value'][ind]

        #Try to find the index of the country's name in the main DataFrame
        #If TypeError, create a new row in the main DataFrame
        try:
            rowNumber = int(dataFrame.loc[dataFrame.isin([lifeSatisfaction['Country'][ind]]).any(axis=1)].index.values)
        except TypeError:
            print("Adding new country", "\n")
            dataFrame = dataFrame.append({'Country (Full Name)': lifeSatisfaction['Country'][ind]}, ignore_index=True)

            #Again, tries to find the index of the country's name in the main DataFrame
            rowNumber = int(dataFrame.loc[dataFrame.isin([lifeSatisfaction['Country'][ind]]).any(axis=1)].index.values)

        #If the column is not in the main DataFrame, add it and set all of its values equal to "Nan"
        if header not in list(dataFrame.columns):
            dataFrame.insert(len(list(dataFrame.columns)), str(header), "Nan")

        #Add the value to the main DataFrame at column name and row number
        dataFrame[header][rowNumber] = value

    #Dropping the Columns/Row that are useless
    dataFrame = dataFrame.drop(189)

    #Writes the single DataFrame into a file for easier acess
    dataFrame.to_csv("combinedData.csv", index=False)

    return dataFrame

#Reads the combinedDataFile for easier acess
def readCleanCSVFile():
    return pd.read_csv("combinedData.csv")

def cleanUpData():
    dataFrame = readCleanCSVFile()

    print("Total Countries: ", len(list(dataFrame.index)))

    removeList = []

    for rowIndex in dataFrame.index:
        totalNan = 0

        for columnIndex in range(0,len(list(dataFrame.columns))):
            #print(dataFrame.iat[rowIndex, columnIndex])
            if dataFrame.iat[rowIndex, columnIndex] == "Nan":
                totalNan+=1

        #print(str(dataFrame.iat[rowIndex, 0]), " - ", totalNan, " - ", (.5 * len(list(dataFrame.columns))))

        if (totalNan > (.5 * len(list(dataFrame.columns)))):
            removeList.insert(0, rowIndex)

    for item in removeList:
        dataFrame = dataFrame.drop(item)

    print("Total Counrties: ", len(list(dataFrame.index)), "\n")

    print(dataFrame.head())

def main():
    print()
    #importDataFiles()
    cleanUpData()


if __name__ == "__main__":
    main()