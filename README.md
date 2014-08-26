Python
======

Here we post a variety of code related to tracking particles through numerical fields and comparing them to drifter tracks.

The most up-to-date merged code is in "track.py" which uses functions stored in "track_functions.py".

The older version of this code is organized in various subdirectories according to its basic function.

The subdirectory "web_track", for example, contains the work of Jian Cui with a program called "track_cmp.py".
It compares drifter tracks with model tracks and currently works on both FVCOM and ROMS.

The subdirectory "multi_track", for example, contains the work of Conner Warren. It is an extension of Jian's code to plot multiple drifter tracks and, if needed, create a multi-panel figure of the results.

The subdirectory "forecast_track" is the work of Nkosi Muse which applies the above two utility focussed on forecasting drifter tracks.
