import profiles
import util
from os import path

"""
Gaussian x1
"""
dataset_path = path.join("dataset", "howtofit", "chapter_phase_api", "gaussian_x1")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)
