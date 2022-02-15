# Python Testing 2.0 Setup

This document details how to setup Cucumber and Hypothesis for Python.

## Prerequisites
- Python 3
- pip

## Cucumber

1.  Using your preferred method of utilizing pip, run the command `pip install behave`.
2.  Follow the steps in Behave's [tutorial document](https://behave.readthedocs.io/en/stable/tutorial.html). It should give you a good starting baseline.

## Hypothesis

1.  Using your preferred method of utilizing pip, run the command `pip install hypothesis`.
2.  Follow the steps in Hypothesis's [tutorial document](https://hypothesis.readthedocs.io/en/latest/quickstart.html#installing). **Read starting from the *Installing* section downwards, and then once at the bottom, go back up to the [*An example*](https://hypothesis.readthedocs.io/en/latest/quickstart.html#an-example) section.**
3.  Here is a [helpful document](https://fsharpforfunandprofit.com/posts/property-based-testing-2/) for learning more about PBT.

## Local Example

1.  To run the example in this repo, go inside the `features` directory and run the `behave` command.