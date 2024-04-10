// Import data
use "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw.dta", clear

// Set output path
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw9\output"
cd "`outputpath'"


collapse (mean) recyclingrate, by(nyc year)


// Generate line plots for NYC and control
twoway (connected recyclingrate year if nyc, lc(blue)) ///
       (connected recyclingrate year if !nyc, lc(red)), ///
       legend(ring(0) pos(11) order(1 "NYC" 2 "Control") rows(2)) xline(2002 2004) title("Recycling Rate")
graph export "C:\Users\sellison8\Dropbox\phdee\hw9\output\recyclingrate.pdf", replace

// Question 2 setup
use "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw.dta", clear

// Local drop years outside of 1997-2004
local drop_years "year < 1997 | year > 2004"
drop if `drop_years'

// Generate treatment variable
gen treatment=0
replace treatment=1 if nyc & year>2001

// Run twfe
ivreghdfe recyclingrate treatment, absorb(region year) vce(cluster region)

// Question 3 SDID
sdid recyclingrate region year treatment , vce(bootstrap) seed(1) reps(100) graph  ///
	g2_opt(legend(ring(0) pos(11) order(1 "NYC" 2 "Control") region(style(none)) rows(2)))
graph export "C:\Users\sellison8\Dropbox\phdee\hw9\output\sdid.pdf", replace

// Question 4 Event-Study - I have no idea why it is flipped
use "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw.dta", clear

ivreghdfe recyclingrate b2001.yea##1.nyc incomepercapita nonwhite munipop2000 collegedegree2000 democratvoteshare2000 democratvoteshare2004, absorb(region year) vce(cluster region) 
coefplot, baselevels omitted xline(5.5) yline(0) ytitle(Coefficient) keep(*.year#1.nyc) scale(1.5) ///
coeflabels(1997.year#1.nyc= "1997" 1998.year#1.nyc="1998" 1999.year#1.nyc="1999" ///
	2000.year#1.nyc="2000" 2001.year#1.nyc="2001" 2002.year#1.nyc="2002" ///
	2003.year#1.nyc="2003" 2004.year#1.nyc="2004" 2005.year#1.nyc="2005" ///
	2006.year#1.nyc="2006" 2007.year#1.nyc="2007" 2008.year#1.nyc= "2008") ///
	vertical
	
graph export "C:\Users\sellison8\Dropbox\phdee\hw9\output\eventstudy.pdf", replace

// Question 5 Synthetic Control 
use "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw.dta", clear

// Collapse data
collapse (mean) recyclingrate incomepercapita collegedegree2000 democratvoteshare2000 democratvoteshare2004 nonwhite (first) nj ma munipop2000, by(id nyc year)
save "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw_sc.dta", replace

collapse (mean) recyclingrate incomepercapita collegedegree2000 democratvoteshare2000 democratvoteshare2004 nonwhite (first) nj ma id munipop2000, by(nyc year)
drop if !nyc 
save "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw_sc_nyc.dta", replace

use "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw_sc.dta", clear
drop if nyc
append using "C:\Users\sellison8\Dropbox\phdee\hw9\recycling_hw_sc_nyc.dta"

/// SC
la var recyclingrate "Recycling Rate"
xtset id year
synth recyclingrate recyclingrate(1997) recyclingrate(1998) recyclingrate(1999) ///
	recyclingrate(2000) recyclingrate(2001) democratvoteshare2000(2000) collegedegree2000(2000) nonwhite incomepercapita, trunit(27) trperiod(2002) fig keep(scresult) replace
graph export "C:\Users\sellison8\Dropbox\phdee\hw9\output\scgraph.pdf", replace
synth_runner recyclingrate recyclingrate(1997) recyclingrate(1998) recyclingrate(1999) recyclingrate(2000) recyclingrate(2001) democratvoteshare2000(2000) collegedegree2000(2000) nonwhite incomepercapita, trunit(27) ///
mspeperiod(1998(1)2001) gen_vars

single_treatment_graph, treated_name(NYC) trlinediff(-0.5) 
 
	
