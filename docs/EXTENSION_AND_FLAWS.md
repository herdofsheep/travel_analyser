## Not covered:

* No unit checking for entries in emission data
* All distance journeys measured as crow-flight (straight line) trips rather than a realistic route
* Distance checker is a little approximate, assumes earth is a perfect sphere.
* I don't check if currency is GBP before calculating distances from value.
* Check for if trip is in GBR only checks if in London, should be broader with a list of UK airports or similar.
* Would be good to set up specific Exception type classes but seems a bit overkill for limited time
* Could use more logs reporting on stages of processing, just have a couple here and there and they could be more informative.

## What would be good given more time:

* Any visualisations of the chart data
* An output other than just a file, reporting in the terminal perhaps
* Friendlier interface, depending on use case, eg. a web-page or python GUI
* More generalised functions, less specific to this one data set (eg. able to handle Air and Rail price data)
* Long term, an interface for recieving files such as these which enforce some structure and data quality.
* More tests!!! No proper edgecase testing, have only covered a fraction of the code.
* Would be good to cross check values for emission factors data with other sources, understand assumptions etc. Flight emissions per km especially seem suspiciously low.
* Could do with proper explanatory doc strings at the top of each function, only done this in a couple of places