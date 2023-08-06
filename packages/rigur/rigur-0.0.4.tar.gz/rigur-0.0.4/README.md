# rigur

A simple python GUI for ripping data from images of figures (**ri**p fi**gur**e).

## Install 

`pip3 install --user rigur`

# Usage

Call `rigur` from a terminal

1. Open an image of a figure ([see example](https://github.com/dfujim/rigur/blob/master/images/fig3.png) from D. Fujimoto, _et al._ [Chem. Mater. 31, 9346 (2019)](http://doi.org/10.1021/acs.chemmater.9b02864).)
2. Align cursors with tick marks in the figure and enter the corresponding values as in the below example:
<a href="https://github.com/dfujim/rigur/blob/master/images/screenshot.png"><img src="https://raw.githubusercontent.com/dfujim/rigur/master/images/screenshot.png" width="800"></a>
3. Scale axes (in the example, select "Log10" for y-axis). Note that for non-linear axes, the displayed tick marks will be the log of the values.
4. Right-click to collect data
5. Export when ready

Don't forget to zoom to increase accuracy of the above steps
