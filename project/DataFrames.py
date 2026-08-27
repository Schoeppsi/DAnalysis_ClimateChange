import pandas as pd

from Enums import *

#%% helpers

def uniformDf(df):    
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "")
    df = df.apply(lambda col: col.str.lower() if col.dtypes == "object" else col)
    return df.apply(lambda col: col.str.replace(" ","") if col.dtypes == "object" else col)  

def uniformList(strList):
    for i in range(0, len(strList)):
        strList[i] = uniformString(strList[i])
    return strList

def uniformString(string):
    if (type(string) == str):
        string = string.lower()
        return string.replace(" ", "")
    
def DfOfRegion(df, region):
    if (region == Region.World):
        try:
            return df.set_index("entity").loc["world"].reset_index(drop=False)
        except:
            print(f"Region {region} could not be found. Returned None. (Code 1)")
            return None            
            
    if (region == Region.Continents):        
        try:
            return df.set_index("entity").loc[continentList].reset_index(drop=False)
        except: 
            print(f"Region {region} could not be found. Returned None. (Code 2)")
            return None
        
    if (region == Region.Countries):
        try:
            return df.set_index("entity").loc[countryList].reset_index(drop=False)
        except: 
            print(f"Region {region} could not be found. Returned None. (Code 3)")
            return None   
    print(f"Region {region} not implemented. Returned None.")
    return None

def DfOfDisasterType(df, disasterType):
    disType = disasterType.name
    try:
        return df.set_index("entity").loc[disType].reset_index(drop=False)
    except:
        print(f"DisasterType {disType} could not be found.")
        return None

def ApplyYears(df, _startYear):
    if (df is None):
        print("Cannot apply startYear if df is None")
        return None
    df = df[df["year"] >= _startYear].copy()
    df["year_ts"] = pd.to_datetime(df["year"], format="%Y")    
    return df

#%% CONFIG

defaultStartYear = 1900
#
continentList = ["Europe", "Asia", "North America", "South America", "Africa","Australia"]
continentList = uniformList(continentList)
#
countryList = ["Germany"]
countryList = uniformList(countryList)

#%% get CO2

def Get_CO2_Landuse(region, year = defaultStartYear):
    return ApplyYears(DfOfRegion(uniformDf(pd.read_csv("DataSets/co2PerCapita_landuse.csv")), region), year)
    
def Get_CO2_Fossil(region, year = defaultStartYear):
    combi = Get_CO2_LandUseAndFossil(region, year)
    landuse = Get_CO2_Landuse(region, year)
    combi["co2"] -= landuse["co2"]
    return combi
    
def Get_CO2_LandUseAndFossil(region, year = defaultStartYear):
    return ApplyYears(DfOfRegion(uniformDf(pd.read_csv("DataSets/co2PerCapita_combi.csv")), region), year)

#%% get population

def Get_Population(region, year = defaultStartYear):
    return ApplyYears(DfOfRegion(uniformDf(pd.read_csv("DataSets/population.csv")), region), year)

#%% get distasters

def Get_Disasters(disasterType, year = defaultStartYear):
    return ApplyYears(DfOfDisasterType(uniformDf(pd.read_csv("DataSets/disasters.csv")), disasterType), year)

#%% get mean temperatures

def Get_MeanTemp(region, year = defaultStartYear):
    if (region == Region.World):
        return ApplyYears(DfOfRegion(uniformDf(pd.read_csv("DataSets/meanTemp_world.csv")), region), year)
    else:
        return ApplyYears(DfOfRegion(uniformDf(pd.read_csv("DataSets/meanTemp_perCountry.csv")), region), year)
    
    








