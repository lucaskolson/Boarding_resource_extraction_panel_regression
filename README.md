# Boarding_resource_extraction_panel_regression

## Table of Contents

- [Project Overview](#project-overview)
- [Data Sources and Cleaning](#data-sources-and-cleaning)
- [Tools](#tools)
- [Data Analysis](#data-analysis)
- [Results](#results)
- [Recommendations](#recommendations)
- [Limitations](#limitations)
- [References](#references)


### Project Overview
This project is a testing the impact of Native boarding school attendance on various measures of the allotment process on reservations. While previous econometrics studies have looked at the impact of allotment on reservations, this study is the first to explore causality the other direction. This adds to a growing body of statistical analyses on boarding and residential schools by demonstrating endogeniety between measures of boarding school attendance and land management. In particular, it demonstrates many of the losses experienced by tribal nations due to boarding school policies through the erosion of sovereignty over their lands. This study focuses on reservations in western Washington and Oregon between 1910-20, finding that boarding school attendance is a significant predictor of future Indian agency logging revenues from outside contractors, indicating corruption among government officials who levereaged child custody to obtain exploitative contracts for resource extraction on reservations.

### Data Sources and Cleaning
Data for this study is based on official statistics from the U.S. annual report of the Indian Affairs Commissioner. The beginning of the period aligns with the changing federal laws allowing for contract logging on Native reservations, and the study extends until 1920 when the variables of interest are no longer included in the annual reports. Agencies are used as the unit of analysis. This decision is based in large part off the way the data is reported, but also reflects to a certain degree the bureaucratic decision-making process through which the government managed land privatization. In all but two cases, agency boundaries remained constant during this period. In one case, the government dissolved the Roseburg Agency, which spanned the Oregon-California border. This agency was not included in this study. In the other case, in 1914 the government carved the Taholah agency out of the Cushman Agency to survey the Quinault reservation for old-growth logging. For this study, the values for these two agencies are aggregated after 1914 to keep a constant unit of analysis, and a more detailed analysis of the Quinault reservation logging during this period is included in the results. 

### Tools
This analysis was conducted in VScode using python. The following libraries are used:

- pandas
- numpy
- matplotlib.pyplot
- linearmodels
- statsmodels

### Data Analysis

The analysis is conducted using panel regressions where various measures of boarding school attendance are the independent variables and logging revenues are the dependent variables. As control variables, I use measures of the total acreage of allotted and unalloted land in each agency. I also ran numerous other regressions using different dependent variables, but the results are not reported here. 

In this study, I use three regression models to assess the causal impact of boarding schools on reservation logging. The first model assesses the effect of the percentages of children at boarding schools on logging revenues. The independent variable in the second model is  the total number of children boarded. The third model uses the disaggregated numbers based on the type of boarding schools. To assess whether there was a causal impact, rather than just a correlation, I compared the school variables from the previous year to the timber sales of the following year. 

### Results

All three models of the coastal region have sufficiently low p-values for the F-test to accept the hypothesis at the 99% confidence level that these models explain more than a simple average of the dependent variable (i.e. all the independent variables combined are meaningfully explaining logging revenues). Furthermore, all three of the models show significant p-values to indicate that higher boarding school attendance from the previous year increased the annual value of timber cut on reservations the following year. 

Interpreting the coefficients on the boarding school variables explains the size of their impact on subsequent logging revenues.  In model (1), the coefficient for the percentage of children is significant at the 99% level, indicating that each additional percentage of children that are boarded would provide $2,841 for an agency in logging revenues the following year. In model (2), the coefficient for total children boarded is significant at the 95% level, indicating that each additional student would provide, on average, $599.58 in logging revenues for the agency the following year. In model (3), the coefficient for off-reservation boarding schools is significant at the 90% level, indicating that each additional child at an off-reservation boarding school would provide $896.2 of logging revenue for the agency in the following year. The coefficient for on-reservation boarding schools is significant at the 95% level, indicating an  agency would generate $728.69 per child. 

![Screenshot from 2024-05-16 15-34-55](https://github.com/lucaskolson/Boarding_resource_extraction_panel_regression/assets/91341415/c1c6a409-b69f-4c04-93f9-9e355097865a)


### Recommendations
The implications of this study are for future econometric studies of boarding schools to recognize endogeneity between boarding school policies and land management, particularly the allotment process. Future studies could expand to different regions of the country, or aggregate across the country, to explore other mechanisms through which boarding school policies impact tribal nations through an erosion of sovereignty.


### Limitations
This study is limited to the coast of Washington and Oregon. Other regions are not likely to find causal relationships with logging specifically, but potentially in other areas such as mining, or more perhaps more interestingly, land inheritance among boarding school students. The timing of allotment varies across reservations, so different time periods may be warranted for other studies. Lastly, focusing on the reservation level rather than the agency level may provide better nuance in futute studies. 

### Selective References

Banner, Stuart. How the Indians Lost Their Land: Law and Power on the Frontier. Harvard University Press, 2009. doi:10.4159/9780674020535.

Carlson, Leonard A. Indians, Bureaucrats, and Land : The Dawes Act and the Decline of Indian Farming. Westport, Connecticut: Greenwood Press, 1981.

Dippel, Christian, and Dustin Frye. "The effect of land allotment on Native American households during the assimilation era." In Journal of Economic History, vol. 80, no. 2, pp. 612-612. 32 AVENUE OF THE AMERICAS, NEW YORK, NY 10013-2473 USA: CAMBRIDGE UNIV PRESS, 2020.

FCNL, “Native American Trust Fund: Massive Mismanagement” September 29, 2016. Accessed at : https://www.fcnl.org/updates/2016-09/native-american-trust-fund-massive-mismanagement

Feir, Donna L. "The long‐term effects of forcible assimilation policy: The case of Indian boarding schools." Canadian Journal of Economics/Revue canadienne d'économique 49, no. 2 (2016): 433-480.

Ficken, Robert E. "After the Treaties: Administering Pacific Northwest Indian Reservations." Oregon Historical Quarterly 106, no. 3 (2005): 442-461.

Gregg, Matthew T. "The long-term effects of American Indian boarding schools." Journal of Development Economics 130 (2018): 17-32.

Hill, James D., and Howard G. Arnett. "Understanding Indian Tribal Timber Sales." Natural Resources & Environment 9, no. 3 (1995): 38-70.

Kelly, David, and Gary Braasch. Secrets of the old growth forest. No. Rev. ed. 1990.

Leonard, Bryan, Dominic P. Parker, and Terry L. Anderson. "Land quality, land rights, and indigenous poverty." Journal of Development Economics 143 (2020): 102435.

MacDonnel, Jake. “Division and Restoration: A Brief History of Forestry on the Quinault Indian Reservation”  Forest History Society, April 2021. Accessed at: https://foresthistory.org/digital-collections/forestry-and-quinault-indian-nation/

Newell, Alan S., Richmond L. Clow, and Richard N. Ellis. A Forest in Trust : Three-Quarters of a Century of Indian Forestry, 1910-1986. Washington, D.C: The Division, 1986.

Newland, Bryan Todd. Federal Indian boarding school initiative investigative report. United States Department of the Interior, Office of the Secretary, 2022.

Portrait of Our Land : A Quinault Tribal Forestry Perspective. Taholah, Wash: Quinault Tribe, 1978.

Quinault Natural Resources. “A Logging History of the Quinault Reservation” Quinault Natural Resources, Winter, 1984.

