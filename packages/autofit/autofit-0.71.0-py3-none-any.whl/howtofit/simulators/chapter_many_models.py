import profiles
import util
from os import path

"""
Gaussian x1
"""
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""
Gaussian x1 with feature
"""
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
gaussian_feature = profiles.Gaussian(centre=70.0, intensity=0.3, sigma=0.5)
util.simulate_line_from_profiles(profiles=[gaussian, gaussian_feature
                                           ], dataset_path=dataset_path)

"""Gaussian x2 split"""
dataset_path = path.join("dataset", "howtofit", "chapter_graphical_models", "gaussian_x2_split")
gaussian_0 = profiles.Gaussian(centre=25.0, intensity=50.0, sigma=12.5)
gaussian_1 = profiles.Gaussian(centre=75.0, intensity=50.0, sigma=12.5)
util.simulate_line_from_profiles(profiles=[gaussian_0, gaussian_1], dataset_path=dataset_path)