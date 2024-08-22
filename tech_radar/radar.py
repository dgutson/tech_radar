"""
tech_radar
Copyright (C) 2024 Daniel Gutson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import random
from typing import Final
import yaml
import matplotlib.pyplot as plt
from matplotlib.projections.polar import PolarAxes
import numpy as np

__VERSION__ : Final = '1.0.0'

class Quadrants:
    def __init__(self, quadrants: int) -> None:
        self.quadrants : Final = quadrants
        self.angle_per_quadrant : Final = 360 / quadrants
        self.tech_count = 0

    def get_center_angle(self, quadrant_number: int) -> float:
        return np.radians(self.angle_per_quadrant * (quadrant_number + 0.5))

    def get_starting_angle(self, quadrant_number: int) -> float:
        return np.radians(self.angle_per_quadrant * quadrant_number)

    def random_angle(self, quadrant_number: int) -> float:
        min_angle = np.radians(self.angle_per_quadrant * (quadrant_number + 0.1))
        max_angle = np.radians(self.angle_per_quadrant * (quadrant_number + 0.9))
        return random.uniform(min_angle, max_angle)

    def set_tech_count(self, new_count: int) -> None:
        self.tech_count = new_count

    def get_tech_angle(self, quadrant_number: int, tech_index: int) -> float:
        inner_angle = self.angle_per_quadrant / (self.tech_count + 1)
        return self.get_starting_angle(quadrant_number) + np.radians(inner_angle * (tech_index + 1))

def random_radius(category: int) -> float:
    min_radius = category + 0.2
    max_radius = category + 0.8
    return random.uniform(min_radius, max_radius)

def draw_chart(categories: list[str], quadrants: list[str]) -> PolarAxes:
    ax: PolarAxes

    qs = Quadrants(len(quadrants))

    _, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'}) # type: ignore

    # Set the radar chart attributes)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, len(categories))  # Set the radial limit to the number of categories

    # Add circles for each category (e.g., Adopt, Trial, Assess, Hold)
    ax.set_yticks(range(1, len(categories) + 1))
    ax.set_yticklabels([])

    for i, label in enumerate(categories):
        angle = np.degrees(np.pi / 2)  # Adjust the angle as needed
        ax.text(0, i + 0.5, label, rotation=0, ha='center', fontweight='bold')
        ax.text(np.pi / 2, i + 0.5, label, rotation=0, ha='center', fontweight='bold')


    # Draw dotted lines to separate each quadrant
    for i in range(len(quadrants)):
        angle = qs.get_starting_angle(i)    #np.radians(i * angle_per_quadrant)
        ax.plot([angle, angle], [0, len(categories)], linestyle='--', color='gray')

    # Add labels for the quadrants, placing them further outside the chart
    label_radius = len(categories) + 1.5  # Increase this value to push labels further out
    for i, quadrant in enumerate(quadrants):
        angle = qs.get_center_angle(i)
        ax.text(angle, label_radius, quadrant, ha='center', va='center', fontsize=12, fontweight='bold', transform=ax.transData)

    # Remove default angular labels and ticks
    ax.set_xticks([])

    return ax

def get_tech_data(tech: dict[str,str] | str) -> tuple[str, str]:
    if isinstance(tech, dict):
        tech_name = list(tech.keys())[0]
        tech_status = tech[tech_name]
        match tech_status:
            case 'incoming':
                symbol = '^'
            case 'outgoing':
                symbol = 'v'
            case _:
                print(f"Unknown tech status {tech_status}, should be 'incoming' or 'outgoing'")
                symbol = 'o'
        return tech_name, symbol
    return tech,'o'

def draw_techs(ax: PolarAxes, quadrants: list[str], categories: list[str], technologies_info: dict) -> None:
    qs = Quadrants(len(quadrants))
    # Iterate over the new hierarchy to gather all the technology data
    for quadrant, category_dict in technologies_info.items():
        quadrant_index = quadrants.index(quadrant)
        for category, tech_list in category_dict.items():
            if tech_list is not None:
                category_index = categories.index(category)
                qs.set_tech_count(len(tech_list))
                tech_index = 0
                for tech in tech_list:
                    radius = random_radius(category_index)
                    angle = qs.get_tech_angle(quadrant_number=quadrant_index, tech_index=tech_index)
                    tech_name, symbol = get_tech_data(tech)
                    ax.plot(angle, radius, symbol, label=tech)
                    ax.text(angle, radius, tech_name, ha='center', va='top')
                    tech_index += 1

def create_tech_radar_from_yaml(yaml_data: dict, filename: str) -> int:
    # Extract data from the YAML
    quadrants: Final = yaml_data['quadrants']
    categories: Final = yaml_data['categories']
    technologies_info: Final = yaml_data['technologies']

    try:
        ax = draw_chart(categories, quadrants)
        draw_techs(ax, quadrants, categories, technologies_info)

        # Save the file
        file_extension = os.path.splitext(filename)[1][1:]
        if file_extension == '':
            file_extension = 'svg'
            filename += '.svg'

        plt.savefig(filename, format=file_extension)
        plt.show()
        return 0
    except ValueError as e:
        print(f"Element not found: {e}")
        return 1


# Load YAML and create the tech radar
def load_yaml_and_create_tech_radar(yaml_file: str, output_file: str) -> int:
    try:
        with open(yaml_file, 'r', encoding='UTF-8') as file:
            yaml_data = yaml.safe_load(file)
        return create_tech_radar_from_yaml(yaml_data, output_file)
    except FileNotFoundError:
        print(f"File not found: {yaml_file}")
        return 1

def main() -> int:
    parser = argparse.ArgumentParser(description="Parse tech radar parameters.")

    parser.add_argument('--size', type=int, default=12, help="Tech radar size")
    parser.add_argument('--min-radius', dest='min_radius', type=float, default=0.1, help="Minimum for random radius")
    parser.add_argument('--max-radius', dest='max_radius', type=float, default=0.9, help="Maximum for random radius")
    parser.add_argument('--input-yaml', dest='input_yaml', type=str, default='tech_radar.yml', help="Name of the input file")
    parser.add_argument('--output', type=str, default='tech_radar.svg', help="Name of the output file")
    parser.add_argument('--version', action='version', version=f"%(prog)s {__VERSION__}")

    args = parser.parse_args()

    return load_yaml_and_create_tech_radar(yaml_file=args.input_yaml, output_file=args.output)

if __name__ == "__main__":
    main()
