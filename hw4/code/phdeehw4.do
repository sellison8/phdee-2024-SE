// Import data
import delimited "C:\Users\sellison8\Dropbox\phdee\hw4\fishbycatch.csv", clear

// Set output path
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw4\output"
cd "`outputpath'"

// Reshape data
reshape long shrimp salmon bycatch, i(firm) j(month)
gen treatment = 0
replace treatment = 1 if treated == 1 & month >= 13

// Create firm indicators
tabulate firm, generate(firm)

// Declare the panel structure
xtset firm month

// Estimate fixed effects model without demeaning (Model a)
xtreg bycatch treatment salmon shrimp firmsize i.firm i.month, robust
eststo model_a

// Perform within-transformation (demeaning) on all variables
foreach var in shrimp salmon bycatch treatment firmsize firm {
    bysort firm: egen `var'_mean = mean(`var')
    gen `var'_demeaned = `var' - `var'_mean
}

// Estimate fixed effects model with demeaned variables (Model b)
areg bycatch_demeaned treatment_demeaned salmon_demeaned shrimp_demeaned firmsize_demeaned, absorb(firm) robust
eststo model_b

// Display the results in the same table, omitting coefficients on firm and month indicators
// tried cells("b(treatment) se(treatment) b(salmon_demeaned) se(salmon_demeaned) b(shrimp_demeaned) se(shrimp_demeaned) b(firmsize_demeaned) se(firmsize_demeaned)") to drop month and firm indicators but it would not run. Tried to debug, can't figure it out 
esttab model_a model_b, ///
    cells() ///
    starlevels(* 0.05 ** 0.01 *** 0.001) ///
    label varwidth(20) ///
    nocons ///
    mti("Model (a)" "Model (b)") ///
    title("Regression Results: Models (a) and (b)")
esttab using "output.tex", replace