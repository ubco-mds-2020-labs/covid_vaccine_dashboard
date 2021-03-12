# [USA & Canada COVID-19 Vaccination Rollout Dashboard](https://covid-vaccine-dashboard.herokuapp.com)

## What are we doing?
### The problem
The status and progress of the COVID-19 vaccination rollout is of great public interest. Thus far, Canada's progress has lagged behind that of the United States on a per-capita basis. This has led the current administration to come under increasing scrutiny, as the public grows eager for a return to normalcy after enduring almost a full year of the pandemic. This creates a need for easy access to hard data on vaccination progress.

### The solution
Creating a comprehensive dashboard outlining the state and provincial-level vaccination rollout across both Canada and the US gives the public a way to keep themselves informed on this important issue without having to sift through traditional news media coverage. By including data for both Canada and the US in one place, users will be able to not only compare how their state/province is doing relative to the national average, but also how their nation as a whole is doing in comparison to their neighbor. Given that Canada is often compared against the United States, we feel that our dashboard will add value in comparison to what currently exists by including detailed data for both nations in one place.

Beyond this, such a dashboard could eventually be used to reflect on the impact of anti-vaccination sentiment on vaccine administration. While the main constraint is currently supply, as COVID vaccines become more widely available in the coming months, questions surrounding the public's willingness to take a vaccination will become relevant. Given that a more complete return to normalcy is predicated on achieving herd immunity through widespread vaccination, it will be useful to offer individuals an easy way to compare administration rates across different localities.

## Where does the data come from?
- Vaccination data for the United States is obtained from [Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations)
- Vaccination data for Canada is obtained from the [COVID-19 Canada Open Data Working Group](https://github.com/ccodwg/Covid19Canada/)

## Description of the App
Our dashboard contains a landing page that shows a choropleth map of the United States and Canada containing the current population-adjusted cumulative vaccination administration for each state/province (as defined by the total number of vaccinations administered divided by population). It includes interactive line plots showing both the cumulative population-adjusted vaccination rates as well as the 7-day rolling mean of the daily chance in vaccinations for any given state/province, along with a comparison to the national average, based on a map-click. Users select particular localities using either a drop-down menu or by clicking a particular region on the map. Below, there is a section where users can make more detailed comparisons of specific metrics across specific localities, e.g. "Daily population-adjusted rolling mean of vaccination distribution for California vs. New York".
