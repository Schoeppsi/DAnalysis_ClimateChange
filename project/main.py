import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import DataFrames as dfs
import Enums as en

#%% No normations

def CO2VsDisasters1():
    # > GET DATAFRAMES
    co2_fossil_world = dfs.Get_CO2_Fossil(en.Region.World)
    pop_world = dfs.Get_Population(en.Region.World)
    #
    dstr_extrTemp = dfs.Get_Disasters(en.DisasterType.extrtemperature)
    dstr_extrweather = dfs.Get_Disasters(en.DisasterType.extrweather)
    dstr_wildfire = dfs.Get_Disasters(en.DisasterType.wildfire)
    dstr_earthquakes = dfs.Get_Disasters(en.DisasterType.earthquake)
    dstr_flood = dfs.Get_Disasters(en.DisasterType.flood)

    # adjusting
    #   from co2 per person -> total co2 by muliplying with population
    co2_fossil_world = co2_fossil_world.merge(pop_world[["year", "population"]], on="year", how="left")
    co2_fossil_world["co2_total"] = co2_fossil_world["co2"] * co2_fossil_world["population"]

    # indexing
    #   use datetime as index, so zooming into data shows months/days etc
    co2_fossil_world = co2_fossil_world.set_index("year_ts")
    dstr_extrTemp = dstr_extrTemp.set_index("year_ts")
    dstr_earthquakes = dstr_earthquakes.set_index("year_ts")
    dstr_wildfire = dstr_wildfire.set_index("year_ts")
    dstr_extrweather = dstr_extrweather.set_index("year_ts")
    dstr_flood = dstr_flood.set_index("year_ts")

    # plotting
    fig, axL = plt.subplots()
    axR = axL.twinx()

    # right axis
    axL.plot(co2_fossil_world.index, co2_fossil_world["co2_total"], color="black", linewidth=1)
    axL.fill_between(co2_fossil_world.index, np.zeros(len(co2_fossil_world.index)), co2_fossil_world["co2_total"],
                     color=(0.35,0.35,0.35), label=r"$CO_2 emissions$")

    # left axis
    axR.plot(dstr_flood.index, dstr_flood["disasters"], color="lightblue", label="Floods")
    axR.plot(dstr_extrweather.index, dstr_extrweather["disasters"], color="blue", label="Extreme weather")
    axR.plot(dstr_extrTemp.index, dstr_extrTemp["disasters"], color="red", label="Extreme temperatures")
    axR.plot(dstr_earthquakes.index, dstr_earthquakes["disasters"], color="black", label="Earthquakes")
    axR.plot(dstr_wildfire.index, dstr_wildfire["disasters"], color="orange", label="Wildfires")
    #

    # further adjustments
    axR.set_title(r"Worldwide delelopement of $CO_2$ emission and disasters," "\nin total quantities.")
    axR.set_xlabel("Year")
    axR.set_ylabel("Disasters")
    plt.xlim(co2_fossil_world.index.min(), co2_fossil_world.index.max())
    axR.set_ylim([0,250])
    
    #
    axL.set_ylabel(r"$CO_2$ emission worldwide")
    axL.set_ylim([0,4E10])

    # legend
    handles_axL, labels_axL = axL.get_legend_handles_labels()
    handles_axR, labels_axR = axR.get_legend_handles_labels()
    axL.legend(handles_axL + handles_axR, labels_axL + labels_axR, loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.show()    
    
#%% annual

def CO2VsDisasters2():
    # > GET DATAFRAMES
    co2_fossil_world = dfs.Get_CO2_Fossil(en.Region.World)
    pop_world = dfs.Get_Population(en.Region.World)
    #
    dstr_extrTemp = dfs.Get_Disasters(en.DisasterType.extrtemperature)
    dstr_extrweather = dfs.Get_Disasters(en.DisasterType.extrweather)
    dstr_wildfire = dfs.Get_Disasters(en.DisasterType.wildfire)
    dstr_earthquakes = dfs.Get_Disasters(en.DisasterType.earthquake)
    dstr_flood = dfs.Get_Disasters(en.DisasterType.flood)

    # adjusting
    #   from co2 per person -> total co2 by muliplying with population
    co2_fossil_world = co2_fossil_world.merge(pop_world[["year", "population"]], on="year", how="left")
    co2_fossil_world["co2_total"] = co2_fossil_world["co2"] * co2_fossil_world["population"]
    #   use data mean from 1900-1920 as normating constant
    co2_fossil_world["co2_total_normed"] = co2_fossil_world["co2_total"] / co2_fossil_world[(1900 <= co2_fossil_world["year"]) & (co2_fossil_world["year"] <= 1920)]["co2_total"].mean()
    #
    dstr_extrweather["disasters_normed"] = dstr_extrweather["disasters"] / dstr_extrweather[(1900 <= dstr_extrweather["year"]) & (dstr_extrweather["year"] <= 1920)]["disasters"].mean()
    dstr_wildfire["disasters_normed"] = dstr_wildfire["disasters"] / dstr_wildfire[(1900 <= dstr_wildfire["year"]) & (dstr_wildfire["year"] <= 1920)]["disasters"].mean()
    dstr_earthquakes["disasters_normed"] = dstr_earthquakes["disasters"] / dstr_earthquakes[(1900 <= dstr_earthquakes["year"]) & (dstr_earthquakes["year"] <= 1920)]["disasters"].mean()
    dstr_flood["disasters_normed"] = dstr_flood["disasters"] / dstr_flood[(1900 <= dstr_flood["year"]) & (dstr_flood["year"] <= 1920)]["disasters"].mean()
    dstr_extrTemp["disasters_normed"] = dstr_extrTemp["disasters"] # temp
    
    # indexing
    #   use datetime as index, so zooming into data shows months/days etc
    co2_fossil_world = co2_fossil_world.set_index("year_ts")
    dstr_extrTemp = dstr_extrTemp.set_index("year_ts")
    dstr_earthquakes = dstr_earthquakes.set_index("year_ts")
    dstr_wildfire = dstr_wildfire.set_index("year_ts")
    dstr_extrweather = dstr_extrweather.set_index("year_ts")
    dstr_flood = dstr_flood.set_index("year_ts")

    # plotting
    fig, axL = plt.subplots()
    axR = axL.twinx()

    # right axis
    axL.plot(co2_fossil_world.index, co2_fossil_world["co2_total_normed"], color="black", linewidth=1)
    axL.fill_between(co2_fossil_world.index, np.zeros(len(co2_fossil_world.index)), co2_fossil_world["co2_total_normed"],
                     color=(0.35,0.35,0.35), label=r"$CO_2 emissions$")

    # left axis
    axR.plot(dstr_flood.index, dstr_flood["disasters_normed"], color="lightblue", label="Floods")
    axR.plot(dstr_extrweather.index, dstr_extrweather["disasters_normed"], color="blue", label="Extreme weather")
    axR.plot(dstr_extrTemp.index, dstr_extrTemp["disasters_normed"], color="red", label="Extreme temperatures")
    axR.plot(dstr_earthquakes.index, dstr_earthquakes["disasters_normed"], color="black", label="Earthquakes")
    axR.plot(dstr_wildfire.index, dstr_wildfire["disasters_normed"], color="orange", label="Wildfires")

    # further adjustments
    axR.set_title(r"Worldwide delelopement of $CO_2$ emission and disasters," "\nnormed by the mean of 1900-1920")
    axR.set_xlabel("Year")
    axR.set_ylabel(r"Disasters (in $100\%$)")
    plt.xlim(co2_fossil_world.index.min(), co2_fossil_world.index.max())
    axR.set_ylim([0,200])
    #
    axL.set_ylabel(r"$CO_2$ emission worldwide (in $100\%$)")
    axL.set_ylim([0,15])

    # legend
    handles_axL, labels_axL = axL.get_legend_handles_labels()
    handles_axR, labels_axR = axR.get_legend_handles_labels()
    axR.legend(handles_axL + handles_axR, labels_axL + labels_axR, loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.show()
    


#%% annual + normed

def CO2VsDisasters3():
    # > GET DATAFRAMES
    co2_fossil_world = dfs.Get_CO2_Fossil(en.Region.World)
    pop_world = dfs.Get_Population(en.Region.World)
    #
    dstr_extrTemp = dfs.Get_Disasters(en.DisasterType.extrtemperature)
    dstr_extrweather = dfs.Get_Disasters(en.DisasterType.extrweather)
    dstr_wildfire = dfs.Get_Disasters(en.DisasterType.wildfire)
    dstr_earthquakes = dfs.Get_Disasters(en.DisasterType.earthquake)
    dstr_flood = dfs.Get_Disasters(en.DisasterType.flood)

    # adjusting
    #   from co2 per person -> total co2 by muliplying with population
    co2_fossil_world = co2_fossil_world.merge(pop_world[["year", "population"]], on="year", how="left")
    co2_fossil_world["co2_total"] = co2_fossil_world["co2"] * co2_fossil_world["population"]
    #   use data mean from 1900-1920 as normating constant
    co2_fossil_world["co2_total_normed"] = co2_fossil_world["co2_total"] / co2_fossil_world[(1900 <= co2_fossil_world["year"]) & (co2_fossil_world["year"] <= 1920)]["co2_total"].mean()
    #
    dstr_extrweather["disasters_normed"] = dstr_extrweather["disasters"] / dstr_extrweather[(1900 <= dstr_extrweather["year"]) & (dstr_extrweather["year"] <= 1920)]["disasters"].mean()
    dstr_wildfire["disasters_normed"] = dstr_wildfire["disasters"] / dstr_wildfire[(1900 <= dstr_wildfire["year"]) & (dstr_wildfire["year"] <= 1920)]["disasters"].mean()
    dstr_earthquakes["disasters_normed"] = dstr_earthquakes["disasters"] / dstr_earthquakes[(1900 <= dstr_earthquakes["year"]) & (dstr_earthquakes["year"] <= 1920)]["disasters"].mean()
    dstr_flood["disasters_normed"] = dstr_flood["disasters"] / dstr_flood[(1900 <= dstr_flood["year"]) & (dstr_flood["year"] <= 1920)]["disasters"].mean()
    dstr_extrTemp["disasters_normed"] = dstr_extrTemp["disasters"] # temp
    
    # temp indexing
    #   use datetime as index, so zooming into data shows months/days etc
    co2_fossil_world = co2_fossil_world.set_index("year")
    dstr_extrTemp = dstr_extrTemp.set_index("year")
    dstr_earthquakes = dstr_earthquakes.set_index("year")
    dstr_wildfire = dstr_wildfire.set_index("year")
    dstr_extrweather = dstr_extrweather.set_index("year")
    dstr_flood = dstr_flood.set_index("year")  
    
    #   use mean of +-5 years data from earthquakes to approx. increase of disaster report rates over years
    for y in range(1900, 2025): # latest data is from 2024
        vals = []
        for _y in range(y-5, y+6):
            if _y < 1900 or 2025 <= _y or _y not in dstr_earthquakes.index:
                continue
            vals.append(dstr_earthquakes.loc[_y, "disasters_normed"])
        if y in dstr_extrweather.index:
            dstr_extrweather.loc[y, "disasters_normed2"] = dstr_extrweather.loc[y, "disasters_normed"] / np.mean(vals)
        if y in dstr_wildfire.index:
            dstr_wildfire.loc[y, "disasters_normed2"] = dstr_wildfire.loc[y, "disasters_normed"] / np.mean(vals)
        if y in dstr_flood.index:
            dstr_flood.loc[y, "disasters_normed2"] = dstr_flood.loc[y, "disasters_normed"] / np.mean(vals)
        if y in dstr_extrTemp.index:
            dstr_extrTemp.loc[y, "disasters_normed2"] = dstr_extrTemp.loc[y, "disasters_normed"] / np.mean(vals)  
    
    # indexing
    #   use datetime as index, so zooming into data shows months/days etc
    co2_fossil_world = co2_fossil_world.reset_index().set_index("year_ts")
    dstr_extrTemp = dstr_extrTemp.reset_index().set_index("year_ts")
    dstr_earthquakes = dstr_earthquakes.reset_index().set_index("year_ts")
    dstr_wildfire = dstr_wildfire.reset_index().set_index("year_ts")
    dstr_extrweather = dstr_extrweather.reset_index().set_index("year_ts")
    dstr_flood = dstr_flood.reset_index().set_index("year_ts")
    
    # plotting
    fig, axL = plt.subplots()
    axR = axL.twinx()

    # right axis
    axL.plot(co2_fossil_world.index, co2_fossil_world["co2_total_normed"], color="black", linewidth=1)
    axL.fill_between(co2_fossil_world.index, np.zeros(len(co2_fossil_world.index)), co2_fossil_world["co2_total_normed"],
                     color=(0.35,0.35,0.35), label=r"$CO_2 emissions$")

    # left axis
    
    axR.plot(dstr_flood.index, dstr_flood["disasters_normed2"], color="lightblue", label="Floods")
    axR.plot(dstr_extrweather.index, dstr_extrweather["disasters_normed2"], color="blue", label="Extreme weather")
    axR.plot(dstr_extrTemp.index, dstr_extrTemp["disasters_normed2"], color="red", label="Extreme temperatures")
    axR.plot(dstr_wildfire.index, dstr_wildfire["disasters_normed2"], color="orange", label="Wildfires")

    # further adjustments
    axR.set_title(r"Worldwide development of CO₂ emissions and disasters," "\nexcluding the approximate influence of sparse data,\nnormalized by the mean of 1900–1920.")
    axR.set_xlabel("Year")
    axR.set_ylabel(r"Disasters (in $100\%$)")
    plt.xlim(co2_fossil_world.index.min(), co2_fossil_world.index.max())
    axR.set_ylim([0,30])
    #
    axL.set_ylabel(r"$CO_2$ emission worldwide (in $100\%$)")
    axL.set_ylim([0,15])

    # legend
    handles_axL, labels_axL = axL.get_legend_handles_labels()
    handles_axR, labels_axR = axR.get_legend_handles_labels()
    axL.legend(handles_axL + handles_axR, labels_axL + labels_axR, loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.show()
    

#%% execution

CO2VsDisasters1()   # absolute values
CO2VsDisasters2()   # annual values
CO2VsDisasters3()   # normed annual values

















