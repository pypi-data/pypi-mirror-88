import examplecurves
from arithmeticmeancurve import ArithmeticMeanCurve

sample_curves = examplecurves.Static.create(
    family_name="nonlinear0", predefined_offset=1
)
a_mean_curve = ArithmeticMeanCurve(sample_curves)

import matplotlib.pyplot as plt

# Setup figure
fig = plt.figure(figsize=(10, 5), dpi=96)
gspec = fig.add_gridspec(1, 1)
axis = fig.add_subplot(gspec[:, :])
axis.set_title("extrapolated arithmetic mean curve")
# Plot
for index, (label, curve) in enumerate(a_mean_curve.family_of_curves.iteritems()):
    current_label = "sample curve {}".format(index)
    axis.plot(curve, marker="o", markersize=3, label=current_label)
axis.plot(a_mean_curve.mean_curve, "--ko", markersize=5, label="arithmetic mean curve")
axis.plot(a_mean_curve.std_circle, ":r", label="std circle")
axis.plot(a_mean_curve.scatter_curve, ":k", label="scatter curve")

# Finishing touch
axis.legend()
plt.tight_layout()
plt.show()