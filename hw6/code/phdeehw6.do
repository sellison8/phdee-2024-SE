clear
// Import data
use "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered.dta", clear 

// Set output path
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw6\output"
cd "`outputpath'"

gen double time= clock(datetime, "MDYhms")
format time %tc
order time id treatment

// Generate treatment cohort manual
	bysort id treatment: egen first_treated=min(time) if treatment==1
	bysort id (first_treated): replace first_treated=first_treated[1] if missing(first_treated)
	format first_treated %tc
// Generate treatment cohort variable using canned procedure from csdid
	egen cohort=csgvar(treatment), ivar(id) tvar(time)
	format cohort %tc
// Generate hour
sort time
egen hour=seq(), by(id)

// save hourly data
save "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered_hr.dta", replace

// Estimate TWFE weights
twowayfeweights energy cohort hour treatment, type(feTR)

// TWFE DiD
use "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered_hr.dta", clear
est clear
eststo: reghdfe energy treatment temperature precipitation relativehumidity, absorb(time id) vce(cluster id)

// Export results
esttab using "C:\Users\sellison8\Dropbox\phdee\hw6\output\hourly_twfe.tex", label replace ///
	b(4) se(4) ////
	collabels(none) star(* 0.10 ** 0.05 *** 0.01) nonum ///
	coeflabels(treatment "ATT" relativehumidity "Relative Humidity" ) ///
	ar2 sfmt (%8.2f)
	
// Question 2
// Load data
use "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered_hr.dta", clear

// Collapse to daily 
gen date=dofc(time)
format date %td
collapse (max) treatment=treatment (sum) energy=energy (mean) temperature precipitation relativehumidity zip size occupants devicegroup, by(id date)

// Generate day
sort date 
egen day=seq(), by(id)

// Generate cohort 
bysort id treatment: egen first_treated=min(day) if treatment==1
bysort id (first_treated): replace first_treated=first_treated[1] if missing(first_treated)

// Save daily data
save "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered_day.dta", replace

// TWFE DiD
use "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered_day.dta", clear
eststo: reghdfe energy treatment temperature precipitation relativehumidity, absorb(date id) vce(cluster id)

// Export results
esttab using "C:\Users\sellison8\Dropbox\phdee\hw6\output\daily_twfe.tex", label replace ///
	b(4) se(4) ////
	mtitles("Energy consumption (kWh)") collabel(none) star(* 0.10 ** 0.05 *** 0.01) nonum ///
	coeflabels(treatment "ATT" relativehumidity "Relative Humidity (\%)" temperature "Temperature (F)" precipitation "Precipitation (in)" ) ///
		ar2 sfmt(%8.2f)

// Event Study Manual
use "C:\Users\sellison8\Dropbox\phdee\hw6\energy_staggered_day.dta", clear

// Create event_time variable
gen event_time = day - first_treated
	
// Make dummies for period and omit -1 period
char event_time[omit] -1
xi i.event_time, pref(_T)
	
// Position of -2
local pos_of_neg_2 = 28 

// Position of 0
local pos_of_zero = `pos_of_neg_2' + 2

// Position of max
local pos_of_max = `pos_of_zero' + 29

// Event study
reghdfe energy  _T* temperature precipitation relativehumidity, absorb(id) vce(cluster id)
	forvalues i = 1(1)`pos_of_neg_2'{
		scalar b_`i' = _b[_Tevent_tim_`i']
		scalar se_v2_`i' = _se[_Tevent_tim_`i']
	}
		

	forvalues i = `pos_of_zero'(1)`pos_of_max'{
		scalar b_`i' = _b[_Tevent_tim_`i']
		scalar se_v2_`i' = _se[_Tevent_tim_`i']
	}

	capture drop order
	capture drop b 
	capture drop high 
	capture drop low

	gen order = .
	gen b =. 
	gen high =. 
	gen low =.

	local i = 1
	local graph_start  = 1
	forvalues day = 1(1)`pos_of_neg_2'{
		local event_time = `day' - 2 - `pos_of_neg_2'
		replace order = `event_time' in `i'
		
		replace b    = b_`day' in `i'
		replace high = b_`day' + 1.96*se_v2_`day' in `i'
		replace low  = b_`day' - 1.96*se_v2_`day' in `i'
			
		local i = `i' + 1
	}

	replace order = -1 in `i'

	replace b    = 0  in `i'
	replace high = 0  in `i'
	replace low  = 0  in `i'

	local i = `i' + 1
	forvalues day = `pos_of_zero'(1)`pos_of_max'{
		local event_time = `day' - 2 - `pos_of_neg_2'

		replace order = `event_time' in `i'
		
		replace b    = b_`day' in `i'
		replace high = b_`day' + 1.96*se_v2_`day' in `i'
		replace low  = b_`day' - 1.96*se_v2_`day' in `i'
			
		local i = `i' + 1
	}


	return list

twoway rarea low high order if order<=29 & order >= -29 , fcol(gs14) lcol(white) msize(1) /// estimates
		|| connected b order if order<=29 & order >= -29, lw(0.6) col(white) msize(1) msymbol(s) lp(solid) /// highlighting
		|| connected b order if order<=29 & order >= -29, lw(0.2) col("71 71 179") msize(1) msymbol(s) lp(solid) /// connect estimates
		|| scatteri 0 -29 0 29, recast(line) lcol(gs8) lp(longdash) lwidth(0.5) /// zero line 
			xlab(-30(10)30 ///
					, nogrid labsize(2) angle(0)) ///
			ylab(, nogrid labs(3)) ///
			legend(off) ///
			xtitle("Day since receiving treatment", size(5)) ///
			ytitle("Daily energy consumption (kWh)", size(5)) ///
			xline(-.5, lpattern(dash) lcolor(gs7) lwidth(0.6)) 	
			
graph export "C:\Users\sellison8\Dropbox\phdee\hw6\output\event_study.pdf", replace 
	
	
// Event Study Using eventdd
eventdd energy temperature precipitation relativehumidity, hdfe absorb(id) timevar(event_time) cluster(id) graph_op(ytitle("Daily energy consumption (kWh)", size(5)) xlabel(-30(10)30) xtitle("Day since receiving treatment", size(5)))
	
graph export "C:\Users\sellison8\Dropbox\phdee\hw6\output\eventstudy_canned.pdf", replace 
	

twoway rarea low high order if order<=29 & order >= -29 , fcol(gs14) lcol(white) msize(1) /// estimates
		|| connected b order if order<=29 & order >= -29, lw(0.6) col(white) msize(1) msymbol(s) lp(solid) /// highlighting
		|| connected b order if order<=29 & order >= -29, lw(0.2) col("71 71 179") msize(1) msymbol(s) lp(solid) /// connect estimates
		|| scatteri 0 -29 0 29, recast(line) lcol(gs8) lp(longdash) lwidth(0.5) /// zero line 
			xlab(-30(10)30 ///
					, nogrid labsize(2) angle(0)) ///
			ylab(, nogrid labs(3)) ///
			legend(off) ///
			xtitle("Days since receiving treatment", size(5)) ///
			ytitle("Daily energy consumption", size(5)) ///
			xline(-.5, lpattern(dash) lcolor(gs7) lwidth(0.6)) 			
graph export "C:\Users\sellison8\Dropbox\phdee\hw6\output\eventdd.pdf", replace 

// Callaway Sant'Anna DiD
csdid energy temperature precipitation relativehumidity, ivar(id) time (day) gvar(first_treated) wboot reps(50)
estat simple
estat event
csdid_plot, ytitle("Daily energy consumption", size(5)) xlabel(-30(10)30) xtitle("Days since treatment", size(5)) xline(-.5, lpattern(dash) lcolor(gs7) lwidth(0.3))
graph export "C:\Users\sellison8\Dropbox\phdee\hw6\output\\event_study_csdid.pdf", replace
	

