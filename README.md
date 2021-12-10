# Street-Sweeper-Schedule
Mixed Integer Linear Programming to Optimize Street Sweeping Schedule

Using MIP library

[MIP Documentation](https://python-mip.readthedocs.io/en/latest/)

## About the Model

### This model chooses an optimal schedule for a street sweeper to maximize pollution removed over the course of a year. The relevant variables are pollution accumulation rates and precipitation. Please note that this is a very simple version of the model and it will continue to be developed during the next year.

- Objective function is to maximize pollution removed
- Decision variable is choosing which days to sweep. Binary Decision Variable called x
- Constraints
  - No sweeping in January, February, November, and December
  - Sweep at least twice in March and October to capture EOW salts and autumn leaf fall
  - Sweep at least once for the remaining months
  - Cannot sweep more than once within a 10 day span
  - Budget constrains (can change)
- Be sure to download rain_noaa.csv for Providence's Daily Weather Data from 2020

## Model Limitations and Future Work

### This model is part of an ongoing research project, and therefore requires additional data in order to have practical use in the field. Once more data is collected from stormwater field sampling and testing as well as sweeper evaluations, this model will become mroe powerful and useful.

- Accumulation does not reset for days that sweep = 1. This is due to dual dependancy issues, something that I am working on
- Historical rain data is being used, which is not practical for planning future schedules. I am working at developing a probability distribution for precipitation
- I am working on building this model to account for many roads and more than one sweepers. 
- I am working on building this model to account for individual pollutants rather than accumulation as a whole
