# Here examplecurves is used to get exemplary curves.
import examplecurves
curves = examplecurves.Static.create("nonlinear0")

# The actual calculation of the arithmetic mean curve.
from arithmeticmeancurve import ArithmeticMeanCurve
a_mean_curve = ArithmeticMeanCurve(curves=curves)

# Finally the plotting of the mean curve and the sample curves.
import matplotlib.pyplot as plt
plt.plot(a_mean_curve.mean_curve, "-ko", label="arithmetic mean curve")
for label, curve in a_mean_curve.family_of_curves.iteritems():
    plt.plot(curve, "-", label="label")
plt.plot(a_mean_curve.scatter_curve, "--k", label="scatter curve")
plt.plot(a_mean_curve.std_circle, "--r", label="std circle")
plt.legend()
plt.show()