clear
// Import data
import delimited "C:\Users\sellison8\Dropbox\phdee\hw5\instrumentalvehicles.csv", clear

// Set output path
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw5\output"
cd "`outputpath'"
//run regression and weakivtest
est clear
eststo: ivregress liml price car (mpg=weight), robust
	weakivtest
//store resulta
	estadd scalar f_stat=r(F_eff)	
	estadd scalar t_crit=r(c_LIML_5) 
//
	esttab using "estimates_stata.tex", label replace ///
		order(mpg car) keep(mpg car) ///
		b(2) se(2) ////
		mtitle("IV LIML") collabels(none) nostar nonote nonum ///
		coeflabels(mpg "Miles per gallon" car "=1 if the vehicle is sedan") ///
		scalars("f_stat Montiel-Pflueger F-statistics" "t_crit LIML critical value for $\tau=5\%$") obslast


