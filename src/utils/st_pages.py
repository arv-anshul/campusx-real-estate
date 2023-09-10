"""Functions for streamlit app's pages."""


def decorate_options(x):
    x = " ".join(x.split("_")).title()
    x = x.replace("Res", "Residential", 1)
    x = x.replace("Ind", "Independent", 1)
    x = x.replace("Rent", "Rental", 1)
    return x
