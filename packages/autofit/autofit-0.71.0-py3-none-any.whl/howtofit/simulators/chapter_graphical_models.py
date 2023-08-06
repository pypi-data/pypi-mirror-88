import profiles
import util
from os import path

"""Gaussian x1 (0)"""
dataset_path = path.join("dataset", "howtofit", "chapter_graphical_models", "gaussian_x1_0")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=1.0)
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 (1)"""
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=5.0)
dataset_path = path.join("dataset", "howtofit", "chapter_graphical_models", "gaussian_x1_1")
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 (2)"""
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
dataset_path = path.join("dataset", "howtofit", "chapter_graphical_models", "gaussian_x1_2")
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)