***************
Why use csvviz?
***************



Compared to
===========

- pandas:
    - pandas does the heavy lifting but doesn't have much in the way of built in plotting
    - pandas api can be confusing
- altair: csvviz is mostly a leaky abstraction, but Altair still requires writing a little boilerplate code
    - bundling a webpage viz is not straightforward
    - understanding the API vs schema takes some work, to the point that you're practically learning Vega
- seaborn/matplotlib
    - only outputs PNG/SVG, no interactive JS, or exportable into Vega
- learning and writing Vega
    - editing json is annoying
    - boilerplate work to get local bundle setup
    - csvviz provides a convenient scaffold in which you can write all the Vegalite you want
- ggplot2
    - have to learn R
    - only static images: https://ggplot2.tidyverse.org/reference/ggsave.html
    - R is not great for developing command-line apps
- d3
    - d3 is a framework for interaction, not just visualization
