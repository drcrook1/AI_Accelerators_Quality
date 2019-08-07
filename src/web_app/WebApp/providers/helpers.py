"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

def line_to_percent(slope, intercept, x):
    y = intercept + slope * x
    percent = ((y[-1] - y[0]) / y[0]) * 100
    return float(percent)