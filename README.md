# F1 PredictQualifying
Designed for the MLOps Zoomcamp. This repository contains code that we will use to predict the qualifying results based on the practice times. If you are checking out the repo for the purposes of grading for the course please also see the [`grading_cheatsheet.md`](grading_cheatsheet.md)

## What is F1 Qualifying?
F1 is a global motor racing competition, ~20 drivers particpate at each race which takes place typically on a Sunday. However throughout the weekend there are other sessions that take place.

### Race Weekend Structure
* Free Practice 1: This typically occurs on a Friday and lasts for 90 minutes.
* Free Practice 2: Also takes place on a Friday and lasts for 90 minutes.
* Free Practice 3: This takes place on a Saturday morning and lasts for 60 minutes.
* Qualifying: This takes place on Saturday afternoon and sets the starting order for the race on Sunday. Within qualifying there are 3 sub-sessions
    * Q1: This session lasts 15 minutes, and the slowest 5 cars at the end are eliminated (currently 20->15).
    * Q2: This session lasts 15 minutes, and the slowest 5 cars at the end are eliminated (currently 15->10).
    * Q3: Here the 10 remaining cars have 10 minutes to produce the fastest lap possible. This sets the order for the Grid
* Race: This is the main focus and where points are awarded.

NB There are other structures which include sprint races. Currently this format is still in flux and so will not be used for any predictions.

### The Aim
The aim is to take key performance metrics from the three practice sessions and see whether we can predict the qualifying times, and therefore the grid order.

### The Problem
This is more than simply taking the fastest lap that a driver does during the practice session and predicting that. The speed of F1 cars can vary depending on a number of other conditions, for example using more durable but less "grippy" tyres, track conditions such as rain, and also heavier fuel loads can slow a car down. Producing a model that can take all these factors into account cannot be easily calculated.

--> Provide an example? George Russel in Montreal this year?

### The benefits
This is will hopefully be useful in order to assess which cars are actually the fastest. Additionally, if we blind the model to the driver, we can see whether the driver is performing as well as the model predicts. If a driver is consistently outperforming the model one can assume that the driver is faster than the average driver

## Where does the data come from?
F1 produces large numbers of metrics which can be accessed using the [FastF1 python library](https://docs.fastf1.dev/). This in turn uses the [Ergast database](https://ergast.com/mrd/) of current and historical F1 data. NB This will work until the end of 2024, and after that FastF1 will devise a new way of accessing the data.

## How to set it up
### Running Mage

### Data Prep 

### Model Evaluation

### Run current model


