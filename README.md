This code works on .csv generated in ImageJ of a line intensity plot along a cortical capillary in the rodent 
somatosensory cortex from in vivo 2 photon imaging. The vessels selected should be as staight and perpendicular to the axis of raster scanning as 
possible.  The user should select a sutible line width and trace down the center of the vessel and then get an Intensity line profile. 
This should be saved as a .csv file for analysis.
The user will need to record imaging metadata to know the travel time (raster scan line time) and pixel size for esitmation of RBC flux
from this data. For installing ImageJ macros please see: https://imagej.net/ij/developer/macro/macros.html , and for general ImageJ information
see https://imagej.net/ij/.

The second set of code is for python functions for analysis of these Intensity line plots to estimate the number and velocity of RBCs. These 
functions were run in a Goolge CoLabs notebook (https://colab.research.google.com/) running phyton 3. An example of the ops metadata file to
load pixel size and raster scanning times is shown below

For questions please contact Dr. Patrick Reeson, reeson.patrick@gmail.com

Create the ops dict variable in python before running the analysis functions
* Remeber to edit for the specific parameters of your imaging experiemnts *
Define analysis parameter (edit to change conditions)
ops = {
    ###Savitzky-Golay filtering parameters
    'window_length': 5, #
    'polyorder': 2,
    ###Peak detection parameters
    'norm_factor' :  30, # percentile to normalize data
    'height' : 0.0, # minimum height a peak must be
    'width' : 1, # minimum width of peak
    'dist' : 3,  # minimum distance between peaks
    'prom' : 0.005, # difference between adjacent peaks
    ###flux calculation parameters
    't_line' :  3.17, # time of 1 line in rasterscan in ms
    'sanity' : False # boolean for plotting data for sanity checks
}
