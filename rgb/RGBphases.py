import math
import argparse
import json
import csv
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Global phase shift variable
PHASE_SHIFT = 50

def calculate_rgb_values(angle_degrees):
    RGB_max = 255
    adjusted_angle = (angle_degrees + PHASE_SHIFT) % 360
    angle_rad_Red = math.radians(adjusted_angle)
    angle_rad_Green = math.radians(adjusted_angle + 120)
    angle_rad_Blue = math.radians(adjusted_angle + 240)

    Red = round((math.sin(angle_rad_Red) + 1) * (RGB_max / 2))
    Green = round((math.sin(angle_rad_Green) + 1) * (RGB_max / 2))
    Blue = round((math.sin(angle_rad_Blue) + 1) * (RGB_max / 2))

    return Red, Green, Blue

def rgb_to_hex(Red, Green, Blue):
    return "#{:02x}{:02x}{:02x}".format(Red, Green, Blue)

def write_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["angle", "red", "green", "blue", "hex"])
        for row in data:
            writer.writerow(row)

def create_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def create_png_banner(filename, data, dimensions):
    width, height = [int(dim) for dim in dimensions.lower().split('x')]
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    pixels_per_angle = width / len(data)
    for angle, color in enumerate(data):
        x_start = round(angle * pixels_per_angle)
        x_end = round((angle + 1) * pixels_per_angle)
        draw.rectangle([x_start, 0, x_end, height], fill=(color[1], color[2], color[3]))
    image.save(filename)

def create_graph(filename, data):
    angles = [d[0] for d in data]
    Reds = [d[1] for d in data]
    Greens = [d[2] for d in data]
    Blues = [d[3] for d in data]

    plt.figure()
    plt.plot(angles, Reds, 'r-', label='Red')
    plt.plot(angles, Greens, 'g-', label='Green')
    plt.plot(angles, Blues, 'b-', label='Blue')
    plt.title('RGB Values Over Angles')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('RGB Value')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action='store_true', help="Output results to CSV file")
    parser.add_argument("--png", type=str, help="Generate a color banner PNG with specified dimensions, e.g., 500x500")
    parser.add_argument("--graph", action='store_true', help="Generate a graph of RGB values")
    parser.add_argument("--json", action='store_true', help="Output color data to JSON file")
    args = parser.parse_args()

    results = []
    json_data = []
    for angle in range(361):
        Red, Green, Blue = calculate_rgb_values(angle)
        hex_color = rgb_to_hex(Red, Green, Blue)
        results.append([angle, Red, Green, Blue, hex_color])
        json_data.append({"angle": angle, "red": Red, "green": Green, "blue": Blue, "hex": hex_color})

    if args.csv:
        write_to_csv("output.csv", results)
        print("RGB values and hex equivalents have been written to output.csv")

    if args.json:
        create_json_file("colors.json", json_data)
        print("Color data has been written to colors.json")

    if args.png:
        create_png_banner("color_banner.png", results, args.png)
        print(f"Banner image has been saved as color_banner.png with dimensions {args.png}")

    if args.graph:
        create_graph("rgb_graph.png", results)
        print("RGB graph has been saved as rgb_graph.png")

if __name__ == "__main__":
    main()
