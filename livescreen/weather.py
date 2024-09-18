import requests
import cairosvg
import io
import re

def sanitize_svg(svg_content):
    # Remove or correct the problematic float value
    sanitized_svg = re.sub(r"(\d+\.\d+)(r)", r"\1", svg_content.decode('utf-8'))
    return sanitized_svg.encode('utf-8')

def fetch_weather_widget():
    widget_url = "https://www.yr.no/en/content/2-2618425/meteogram.svg?mode=dark"  # copenhagen dark mode svg

    response = requests.get(widget_url)
    
    if response.status_code == 200:
        # Convert SVG to PNG in memory
        try:
            svg_data = sanitize_svg(response.content)
            # print("GOT TO HERE")
            png_data = cairosvg.svg2png(bytestring=svg_data)
            
            # Load the PNG data into a Pygame surface or return it
            png_image = io.BytesIO(png_data)
            return png_image  # Return a BytesIO object containing the PNG data
        except Exception as e:
            print(f"Error converting SVG to PNG: {e}")
            return None
    else:
        print(f"Error fetching SVG: HTTP {response.status_code}")
        return None