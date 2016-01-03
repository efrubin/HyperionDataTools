#!/usr/bin/env python
from sys import exit
from runinfo import *

# Define expressions
# Write color tables
SetCloneWindowOnFirstRef(0)
###############################################################################
width, height = 460, 783
win = GetGlobalAttributes().windows[GetGlobalAttributes().activeWindow]
ResizeWindow(win, width, height)
SetActiveWindow(win) # Synchronize
size = GetWindowInformation().windowSize
if width < size[0] or height < size[1]:
    ResizeWindow(win, width + (size[0] - width), height + (size[1] - height))
DeleteAllPlots()
for name in GetAnnotationObjectNames():
    DeleteAnnotationObject(name)

# Set save attributes
s = SaveWindowAttributes()
s.format = s.PPM
s.width, s.height = width, height
s.fileName = "isoSelfG_" + run + "_density_"
s.outputToCurrentDirectory = 0
s.outputDirectory = "./frames/"
SetSaveWindowAttributes(s)


# Create plots
# Create plot 1
db = "..data/isoSelfG_joined.*.vtk database"
OpenDatabase(db)
AddPlot("Pseudocolor", "density", 0, 0)
atts = PseudocolorAttributes()
atts.colorTableName = "orangehot"
atts.minFlag = 1
atts.min = 1.0e-5
atts.maxFlag = 1
atts.max = 4.0
atts.scaling = atts.Log
SetPlotOptions(atts)
silr = SILRestriction()
silr.TurnOnAll()
SetPlotSILRestriction(silr, 0)

SetActivePlots(0)

DrawPlots()

# Set the view
view = View2DAttributes()
view.windowCoords = (-32, 32, -256, 256)
view.viewportCoords = (0.4, 0.95, 0.15, 0.9)
view.fullFrameActivationMode = view.Auto  # On, Off, Auto
view.fullFrameAutoThreshold = 100
view.xScale = view.LINEAR  # LINEAR, LOG
view.yScale = view.LINEAR  # LINEAR, LOG
view.windowValid = 1
SetView2D(view)

# Set the annotation attributes
annot = AnnotationAttributes()
#SetAnnotationAttributes(annot)

# Set annotation object properties
win0_legend000 = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
win0_legend000.active = 1
win0_legend000.managePosition = 1
win0_legend000.position = (0.05, 0.9)
win0_legend000.xScale = 1
win0_legend000.yScale = 1
win0_legend000.textColor = (0, 0, 0, 255)
win0_legend000.useForegroundForTextColor = 1
win0_legend000.drawBoundingBox = 0
win0_legend000.boundingBoxColor = (0, 0, 0, 50)
win0_legend000.numberFormat = "%# -9.4g"
win0_legend000.fontFamily = win0_legend000.Arial  # Arial, Courier, Times
win0_legend000.fontBold = 0
win0_legend000.fontItalic = 0
win0_legend000.fontShadow = 0
win0_legend000.fontHeight = 0.015
win0_legend000.drawLabels = win0_legend000.Values # None, Values, Labels, Both
win0_legend000.drawTitle = 1
win0_legend000.drawMinMax = 1
win0_legend000.orientation = win0_legend000.VerticalRight  # VerticalRight, VerticalLeft, HorizontalTop, HorizontalBottom
win0_legend000.controlTicks = 1
win0_legend000.numTicks = 5
win0_legend000.minMaxInclusive = 1
win0_legend000.suppliedValues = (1e-05, 0.000251487, 0.00632456, 0.159054, 4)
win0_legend000.suppliedLabels = ()

SetActiveWindow(GetGlobalAttributes().windows[0])

# Cycle through states and save each window

for state in range(start, stop+1):
    SetTimeSliderState(state)
    SaveWindow()

ClearCacheForAllEngines()
DeleteAllPlots()
CloseDatabase(db)
ClearCacheForAllEngines()
CloseComputeEngine()
sys.exit()
