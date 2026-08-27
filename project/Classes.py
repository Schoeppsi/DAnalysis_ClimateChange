import numpy as np
import matplotlib.pyplot as plt

from Enums import *

import math

class Graph:    
    def __init__(self, xVals, yVals):
        self.xVals = xVals
        self.yVals = yVals
        self.color = "black"
        self.label = "--- empty ---"
        #
        self.type = GraphType.Line
    
    def Input_Data(self, xVals, yVals):
        self.xVals = xVals
        self.yVals = yVals
        
    def Set_Label(self, label):
        self.label = label        
    def Set_Color(self, s_color):
        self.color = s_color        
    def Set_Type(self, graphType):
        self.type = graphType
        
     
class Plotter:

    def __init__(self):
        # general
        self.ax1Graphs = []
        self.ax2Graphs = []
        self.title = "--- empty ---"
        self.xLabel = "--- empty ---"
        self.ax1YLabel = "--- empty ---"
        self.ax2YLabel = "--- empty ---"
        # axes
        self.xLim = [-math.inf, math.inf]
        self.ax1YLim = [-math.inf, math.inf]
        self.ax2YLim = [-math.inf, math.inf]
        # colors
        self.xLabelColor = "black"
        self.ax1YLabelColor = "black"
        self.ax2YLabelColor = "black"
        self.xTickColor = "black"
        self.ax1YTickColor = "black"
        self.ax2YTickColor = "black"
        #
        self.showLegend = False
        self.legendPosition = "best"
        self.legendFontSize = 8       
        
    # ---
        
    def Add_Graph(self, graph):
        self.ax1Graphs.append(graph)
        
    def Add_Graph_rightAxis(self, graph):
        self.ax2Graphs.append(graph)
        
    def Remove_Graphs(self):
        self.ax1Graphs = []
    def Remove_Graphs_rightAxis(self):
        self.ax2Graphs = []
    def Remove_AllGraphs(self):
        self.Remove_Graphs()
        self.Remove_Graphs_rightAxis()
        
    # --- 
    
    def Set_title(self, title):
        self.title = title
        
    def Set_xLim(self, xlim):
        self.xLim = xlim
    def Set_yLim(self, ylim):
        self.ax1YLim = ylim
    def Set_yLim_rightAxis(self, ylim):
        self.ax2YLim = ylim
        
    def Set_xLabel(self, xLabel):
        self.xLabel = xLabel
    def Set_yLabel(self, yLabel):
        self.ax1YLabel = yLabel
    def Set_yLabel_rightAxis(self, yLabel):
        self.ax2YLabel = yLabel
    
    def Set_xLabel_color(self, xLabelColor):
        self.xLabelColor = xLabelColor
    def Set_yLabel_color(self, yLabelColor):
        self.ax1YLabelColor = yLabelColor
    def Set_yLabel_rightAxis_color(self, yLabelColor):
        self.ax2YLabelColor = yLabelColor
    
    def Set_xTicks_color(self, xTickColor):
        self.xTickColor = xTickColor
    def Set_yTicks_color(self, yTickColor):
        self.ax1YTickColor = yTickColor
    def Set_yTicks_rightAxis_color(self, yTickColor):
        self.ax2YTickColor = yTickColor
    
    def Set_Legend(self, show, legendPosition, fontSize = 8):
        self.showLegend = show
        self.legendPosition = legendPosition.name.replace("_", " ")
        self.legendFontSize = fontSize
    
    # ---
        
    def Plot(self, DPI):
        
        if (len(self.ax1Graphs) == 0 and len(self.ax2Graphs) == 0):
            print("No graphs assigned to ax1 of plotter. Plotting failed")
            return
        
        fig, ax1 = plt.subplots()

        ax1.set_xlabel(self.xLabel, color=self.xLabelColor)
        ax1.set_ylabel(self.ax1YLabel, color=self.ax1YLabelColor)
        
        ax1.tick_params(axis="x", colors=self.xTickColor)
        ax1.tick_params(axis="y", colors=self.ax1YTickColor)
        
        ax1.set_title(self.title)
        if (self.xLim != [-math.inf, math.inf]):
            ax1.set_xlim(self.xLim)
        if (self.ax1YLim != [-math.inf, math.inf]):
            ax1.set_ylim(self.ax1YLim)
        
        if len(self.ax2Graphs) > 0:
            ax2 = ax1.twinx()
            ax2.set_ylabel(self.ax2YLabel, color=self.ax2YLabelColor)
            ax2.tick_params(axis="y", colors=self.ax2YTickColor)
            if (self.ax2YLim != [-math.inf, math.inf]):
                ax2.set_ylim(self.ax2YLim)
        
        for ax1graph in self.ax1Graphs:
            ax1.plot(ax1graph.xVals, ax1graph.yVals, color=ax1graph.color, label=ax1graph.label)
        for ax2graph in self.ax2Graphs:
            ax2.plot(ax2graph.xVals, ax2graph.yVals, color=ax2graph.color, label=ax2graph.label)
            
        if (self.showLegend):
            handles_ax1, labels_ax1 = ax1.get_legend_handles_labels()
            handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
            ax1.legend(handles_ax1 + handles_ax2, labels_ax1 + labels_ax2, 
                       loc=self.legendPosition, fontsize=self.legendFontSize)
            
        plt.figure(dpi=DPI)
        plt.show()
        
    # ---
    
    
        
        
        
        
        