import profiles
import util
from os import path

"""
Gaussian x1
"""
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 (0)"""
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1_0")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=1.0)
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 (1)"""
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=5.0)
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1_1")
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 (2)"""
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1_2")
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 + Exponential x1"""
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
exponential = profiles.Exponential(centre=70.0, intensity=40.0, rate=0.005)
dataset_path = path.join(
    "dataset", "howtofit", "chapter_1", "gaussian_x1_exponential_x1"
)
util.simulate_line_from_profiles(profiles=[gaussian, exponential], dataset_path=dataset_path)

"""Gaussian x2 + Exponential x1"""
gaussian_0 = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=10.0)
gaussian_1 = profiles.Gaussian(centre=20.0, intensity=30.0, sigma=5.0)
exponential = profiles.Exponential(centre=70.0, intensity=40.0, rate=0.005)
dataset_path = path.join(
    "dataset", "howtofit", "chapter_1", "gaussian_x2__exponential_x1"
)
util.simulate_line_from_profiles(profiles=[gaussian_0, gaussian_1, exponential], dataset_path=dataset_path)

"""Gaussian x3"""
gaussian_0 = profiles.Gaussian(centre=50.0, intensity=20.0, sigma=1.0)
gaussian_1 = profiles.Gaussian(centre=50.0, intensity=40.0, sigma=5.0)
gaussian_2 = profiles.Gaussian(centre=50.0, intensity=60.0, sigma=10.0)
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x3")
util.simulate_line_from_profiles(profiles=[gaussian_0, gaussian_1, gaussian_2], dataset_path=dataset_path)

"""Gaussian x1 unconvolved"""
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1_unconvolved")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=3.0)
util.simulate_line_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)

"""Gaussian x1 convolved"""
dataset_path = path.join("dataset", "howtofit", "chapter_1", "gaussian_x1_convolved")
gaussian = profiles.Gaussian(centre=50.0, intensity=25.0, sigma=3.0)
util.simulate_line_with_kernel_from_gaussian(gaussian=gaussian, dataset_path=dataset_path)