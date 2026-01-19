"""
Placeholder Image Generator Professional Tool.

This module provides a robust CLI interface for generating standardized 
placeholder images used in web development and UI/UX design, specifically 
tailored for requirements like ThemeForest submissions.

Author: AntonBeletsky
License: MIT
Version: 1.0.0
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: The 'Pillow' library is required. Install it using 'pip install Pillow'.")
    sys.exit(1)

# Configure logging for corporate audit trails
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlaceholderGenerator:
    """Handles the creation and styling of placeholder images."""

    def __init__(self, bg_color: str = "#CCCCCC", text_color: str = "#000000"):
        """
        Initialize the generator with corporate branding colors.
        
        Args:
            bg_color (str): Hex code for the image background.
            text_color (str): Hex code for the text overlay.
        """
        self.bg_color = bg_color
        self.text_color = text_color

    def _parse_dimensions(self, size_str: str) -> Tuple[int, int]:
        """
        Extract width and height from various string formats using Regex.
        
        Supported formats: '600x400', '600*400', '600 400'.
        """
        dimensions = re.findall(r'\d+', size_str)
        if len(dimensions) < 2:
            raise ValueError(f"Invalid size format: '{size_str}'. Expected 'Width x Height'.")
        return int(dimensions[0]), int(dimensions[1])

    def generate(self, size_input: str, output_path: str = None) -> str:
        """
        Core logic to render the PNG image.
        
        Args:
            size_input (str): String representation of dimensions.
            output_path (str): Optional custom path for the output file.
            
        Returns:
            str: Path to the generated file.
        """
        try:
            width, height = self._parse_dimensions(size_input)
            label = f"{width} x {height}"
            
            # 1. Create Canvas
            image = Image.new("RGB", (width, height), color=self.bg_color)
            draw = ImageDraw.Draw(image)

            # 2. Dynamic Font Scaling
            # Font size is calculated as 12% of the smallest dimension
            font_size = max(12, int(min(width, height) * 0.12))
            
            try:
                # Common system font paths
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                # Fallback to built-in fixed-size font if system fonts are missing
                logger.warning("System font 'arial.ttf' not found. Falling back to default.")
                font = ImageFont.load_default()

            # 3. Calculate Text Position (Absolute Center)
            # textbbox returns (left, top, right, bottom)
            bbox = draw.textbbox((0, 0), label, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            position = ((width - text_width) // 2, (height - text_height) // 2)

            # 4. Render and Save
            draw.text(position, label, fill=self.text_color, font=font)
            
            final_path = output_path or f"placeholder_{width}x{height}.png"
            image.save(final_path, "PNG")
            
            logger.info(f"Asset generated successfully: {final_path}")
            return final_path

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise

def main():
    """
    Command Line Interface Instruction Manual:
    
    USAGE:
        python placeholder.py <width>x<height> [options]
    
    EXAMPLES:
        1. Basic: python placeholder.py 800x600
        2. Brand Colors: python placeholder.py 1920x1080 --bg #2c3e50 --text #ecf0f1
        3. Custom Output: python placeholder.py 100x100 --out logo_placeholder.png
    """
    parser = argparse.ArgumentParser(
        description="Enterprise Asset Generator for UI Development.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=main.__doc__
    )
    
    parser.add_argument("dimensions", help="Target size (e.g., 600x400)")
    parser.add_argument("--bg", default="#CCCCCC", help="Background Hex (default: #CCCCCC)")
    parser.add_argument("--text", default="#000000", help="Text Hex (default: #000000)")
    parser.add_argument("--out", help="Custom output filename")

    args = parser.parse_args()

    generator = PlaceholderGenerator(bg_color=args.bg, text_color=args.text)
    generator.generate(args.dimensions, args.out)

if __name__ == "__main__":
    main()
