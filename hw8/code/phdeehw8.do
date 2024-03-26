clear
// Import data
use "C:\Users\sellison8\Dropbox\phdee\hw8\electric_matching.dta", clear

// Set output path
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw8\output"
cd "`outputpath'"

// Gen log outcome variable
gen log_mw=ln(mw)

// Gen binary treatment variable
gen treatment = 0
replace treatment=1 if date >mdy(3,1,2020)

// Regression 1a

ivreghdfe log_mw treatment temp pcp, absorb(zone month hour dow)robust

// Regression 1b
encode zone, gen(zone_n)
drop if inrange(month,1,2)

teffects nnmatch (log_mw temp pcp) (treatment), metric(maha) ematch(i.month i.zone_n i.dow i.hour)

// Regression 2a
ivreghdfe log_mw treatment temp pcp, absorb(zone month hour dow year) robust

// Gen year2020 variable 
gen year2020=0
replace year2020=1 if year==2020
drop if year<2019

// Regression 3a 
encode zone, gen(zone_x)
teffects nnmatch (log_mw temp pcp) (year2020), metric(maha) ematch(i.zone_x i.month i.dow i.hour) generate(match) biasadj(temp pcp)
predict log_mw_hat, po tlevel(0)
gen diff_log_mw=log_mw-log_mw_hat
reg diff_log_mw treatment if year2020, robust