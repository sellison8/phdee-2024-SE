ssc install estout, replace
ssc install outreg2
// import data
import delimited "C:\Users\sellison8\Dropbox\phdee\hw2\kwh.csv", clear

// set outputpath
local outputpath "C:\Users\sellison8\Dropbox\phdee\hw2\output"
cd "`outputpath'"
//
eststo treatment: quietly estpost summarize sqft temp if retrofit == 0
eststo control: quietly estpost summarize sqft temp if retrofit == 1
eststo diff: quietly estpost ttest sqft temp, by(retrofit) unequal
esttab treatment control diff, cells("mean(pattern(1 1 0) fmt(3)) sd(pattern(1 1 0)) b(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))") label collabels("Treatment" "Control" "Difference")

// save the table to a .tex file
esttab treatment control diff using statabalance.tex, tex cells("mean(pattern(1 1 0) fmt(3)) sd(pattern(1 1 0)) b(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))"), replace label

// two-way
twoway scatter electricity sqft, xtitle(square feet)
//export plot
graph export twowayscatter.pdf

//regress
regress electricity retrofit sqft temp, robust
outreg2 using myreg.tex, replace label