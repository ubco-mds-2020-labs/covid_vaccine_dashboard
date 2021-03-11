# Reflection

So far, our Dashboard is mostly built-out in alignment with our original vision. There has been some evolution of the layout, and some minor adjustments in scope, but the breadth of functionality and the core components have mostly survived the development process.

We have implemented:

1. Summary statistics for Canada and the USA 
2. An interactive vaccination choropleth map of Canada and the USA
   - Hover shows summary stats and details for each locality (state/priovince)
   - Clicking on localities changes the plots to the left of the map
3. Locality-specific time-series plots to the left of the map, chosen by map-click
   - Top plot shows total vax admin per 100
   - Bottom plot shows daily vax admin per 100 (rolling average)
4. Detailed time-series plot at bottom
   - Provides a more detailed and layered time-series 
   - Responds to multiple user inputs:
     - Region vs. locality
     - Multiple locatilities or regions
     - Raw or per-100
     - Metrics (total vax, daily vax, total distributed, daily distributed)

The dashboard does a good job of achieving our original goals and solving the problem we posed in our proposal. It feels clean, accessible, intuitive, and well laid out. However, the interface could benefit from some polishing, such as:

- Have the bottom plot auto-populate on launch
- Get good alignment and centering between the map and the bottom plot
- Ensure the line colors are consistent for Canada and the US, and that any selected locality line is also a consistent color, matching the blue of the choropleth map.

An interesting aspect that we think would add significant value to our target audience, would be the ability to see this vaccination data in the context of real Covid case data such as confirmed positive tests, or daily new cases, or total estimated cumulative infected persons, etc.