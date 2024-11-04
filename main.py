from mappers.CurveGenerator import CurveGenerator
import random


control_points = [(243, 30, 104), (252, 39, 47), (249, 171, 60), (255, 229, 119), (255, 255, 255)]
curve = CurveGenerator.generate_curve(control_points)
parameter = random.random()
results = []
for _ in range(10):
    results.append(curve.compute_pixel_coordinate(parameter))
    parameter = random.random()

