from trashpanda import cut_dataframe_after

import examplecurves
from arithmeticmeancurve import ArithmeticMeanCurve

sample_curves = examplecurves.create(
    family_name="10",
    offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1],
)
a_mean_curve = ArithmeticMeanCurve(sample_curves)
input_curves = a_mean_curve.family_of_curves.copy()
input_curves = cut_dataframe_after(
    frame_to_cut=input_curves, cutting_index=a_mean_curve.statistics.end_x_mean
)

standard_mean_curve = input_curves.mean(axis=1)



import matplotlib.pyplot as plt

# Setup figure
fig = plt.figure(figsize=(10, 5), dpi=96)
gspec = fig.add_gridspec(2, 5)
curve_axis = fig.add_subplot(gspec[:, :3])
mean_axis = fig.add_subplot(gspec[:, 3:])

curve_axis.set_title("Sample curves")
mean_axis.set_title("Mean curve without extrapolation")
# Plot
for index, curve in enumerate(sample_curves):
    current_label = "Sample curve {}".format(index)
    curve_axis.plot(curve, marker="o", markersize=3, label=current_label)

for index, (label, curve) in enumerate(a_mean_curve.family_of_curves.iteritems()):
    mean_axis.plot(curve, marker="o", markersize=3)
mean_axis.plot(standard_mean_curve, "--ko", markersize=3, label="Standard mean curve")

# Finishing touch
curve_axis.legend(loc="lower right")
mean_axis.legend(loc="lower right")
plt.tight_layout()
plt.show()
