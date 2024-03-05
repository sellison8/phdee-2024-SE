clear
// Import data
import delimited "C:\Users\sellison8\Dropbox\phdee\hw5\instrumentalvehicles.csv", clear

// Set output path
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw7\output"
cd "`outputpath'"
// Run RD
rdrobust mpg length, c(225) p(1) bwselect(mserd)
rdplot mpg length, c(225) p(1) covs(car) genvars ///
graph_options(ytitle(Miles per Gallon) xtitle(Vehicle length (in.))) ///
title("Regression Discontinuity Plot") ///
saving("C:\Users\sellison8\Dropbox\phdee\hw7\rdplot1.pdf", replace)
// Store the predicted values from the first stage
rename rdplot_hat_y mpg_hat

// Hedonic regression in the second stage
regress price mpg_hat car, robust

// Display regression results
di "Average Treatment Effect (ATE) of mpg on Sale Price: " _b[mpg_hat]

