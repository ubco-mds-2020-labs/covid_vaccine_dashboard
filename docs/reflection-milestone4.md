# Reflection - Milestone 4

Our Dashboard is built-out in alignment with our original vision. There has been some evolution of the layout in response to feedback. The breadth of functionality and the core components have mostly survived the development process, and it is now very intuitive and user-friendly.

![img](https://lh3.googleusercontent.com/TC-p0E0FFwUsp8UaC9bsEwB2CaLj0MkQT0OBWlNWPolUXeGwFZS8f5lQkhu2GhtYNCx_AuDnJ6g20GTLJ3AYzKjQNsltqofaztQkq4nrwA9s7kuDwhH7tftsj8R1Uayd8cJQWEil) 

We merge data through Pandas, wrangle using GeoPandas and Calculate new values with Pandas. We use Altair to create our choropleth and line plots. We use Dash to create tabs and selectors, and we deploy on Heroku automatically on pushes to GitHub.

**On Tab 1, we have implemented:**

1. Summary statistics for Canada and the USA
2. An interactive vaccination choropleth map of Canada and the USA
   * Hover shows summary stats and details for each locality (State/Province)
   * Clicking on localities changes the plots to the left of the map and indicates the locality with the colour red
3. Locality-specific time-series plots to the left of the map respond to map-click
   * Top: total vaccination doses administered per 100 residents
   * Bottom: daily doses administered per 100 residents (7-day rolling average)

**On Tab 2, we have implemented:**

A detailed, customizable, time-series plot that:

- Provides a more complex and layered time-series of multiple regions
- Responds to various user inputs: 
  * Region vs. locality
  * Multiple localities or regions 
  * Raw or population-adjusted numbers
  * Metrics (total vax, daily vax, total distributed, daily distributed)

### Feedback

The updated app has been well-received by classmates, family members and friends. Users like the map feature and the ability to do a deep dive and make comparisons between Canada, the USA and sub-regions. Users from both technical and non-technical backgrounds have given us valuable feedback, and we have implemented user feedback to the best of our ability after our initial launch.

1. We created a two-tab system that allows further analysis on the second tab rather than having to scroll down. Metrics that might be confusing to a non-technical user are featured here, which improves user-experience. Tabs also solves the white-space issue that was pointed out by some of our peers.
2. The map now changes colour, indicating that a user has clicked a specific location. The colour is red to suggest the reader look left to the plots generated on the side, which will display the selected locality’s data using a red line.
3. Line colours no longer shift when a new locality is selected by clicking on the map or by using the dropdown on the second tab.

### Future

The dashboard does an excellent job of achieving our original goals and solving the problem we posed in our proposal. It feels clean, accessible, intuitive, and well laid out. However, the interface could benefit from some new features, such as:

Having the plot on the second tab auto-populate on launch

Creating date sliders to zoom in on date ranges of interest

Enabling dynamic plot resizing

Add fully vaccinated people once that data becomes public

Include covid cases to make a one-stop-shop for covid info and contextualize the rollout within the extent pandemic

An interesting aspect that we think would add significant value to our target audience would be seeing this vaccination data in the context of Covid case data, such as confirmed positive tests, or daily new cases, or total estimated cumulative infected persons.