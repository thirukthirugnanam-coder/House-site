#!/usr/bin/env python3
"""
Main script to generate Ayappakkam house layout SVG.
This script orchestrates the layout generation using geometry, dimensions, and labels modules.
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from config import (
    SVG_WIDTH, SVG_HEIGHT, SVG_PADDING,
    COLORS, STROKE_WIDTHS, FONT_SIZES, SCALE_TEXT
)
from geometry import (
    create_svg_root, Rectangle, Ellipse, Text
)
from dimensions import (
    Dimensions, Position,
    PLOT_WIDTH_SVG, PLOT_LENGTH_SVG,
    HOUSE_WIDTH_SVG, HOUSE_LENGTH_SVG,
    GARAGE_WIDTH_SVG, GARAGE_LENGTH_SVG,
    GARDEN_RADIUS_X_SVG, GARDEN_RADIUS_Y_SVG
)
from labels import Label, AreaLabel

class LayoutGenerator:
    """Generate Ayappakkam house layout SVG."""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize layout generator.
        
        Args:
            output_dir: Directory to save the output SVG file
        """
        self.output_dir = output_dir
        self.svg_root = None
        self.dimensions = Dimensions()
        self.position = Position(offset_x=100, offset_y=80)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def create_layout(self) -> ET.Element:
        """Create the complete layout structure."""
        # Create SVG root
        self.svg_root = create_svg_root(SVG_WIDTH, SVG_HEIGHT)
        
        # Add background
        bg = Rectangle(
            0, 0, SVG_WIDTH, SVG_HEIGHT,
            fill=COLORS['background']
        )
        self.svg_root.append(bg.to_element())
        
        # Add title
        title = Label.create_title(SVG_WIDTH / 2, 40, 'Ayappakkam Layout')
        self.svg_root.append(title.to_element())
        
        # Add plot boundary
        self._add_plot_boundary()
        
        # Add house
        self._add_house()
        
        # Add garage
        self._add_garage()
        
        # Add garden
        self._add_garden()
        
        # Add scale information
        self._add_scale_info()
        
        return self.svg_root
    
    def _add_plot_boundary(self):
        """Add plot boundary rectangle."""
        plot = Rectangle(
            100, 80, PLOT_WIDTH_SVG, PLOT_LENGTH_SVG,
            fill=COLORS['plot_fill'],
            stroke=COLORS['plot_stroke'],
            **{'stroke-width': str(STROKE_WIDTHS['plot'])}
        )
        self.svg_root.append(plot.to_element())
        
        # Add plot label
        label_x = 100 + PLOT_WIDTH_SVG / 2
        label_y = 80 + PLOT_LENGTH_SVG + 25
        label = AreaLabel.plot(label_x, label_y)
        self.svg_root.append(label.to_element())
    
    def _add_house(self):
        """Add main house structure."""
        house_x = 150
        house_y = 120
        
        house = Rectangle(
            house_x, house_y, HOUSE_WIDTH_SVG, HOUSE_LENGTH_SVG,
            fill=COLORS['house_fill'],
            stroke=COLORS['house_stroke'],
            **{'stroke-width': str(STROKE_WIDTHS['building'])}
        )
        self.svg_root.append(house.to_element())
        
        # Add house label
        label_x = house_x + HOUSE_WIDTH_SVG / 2
        label_y = house_y + HOUSE_LENGTH_SVG / 2 + 5
        label = AreaLabel.house(label_x, label_y)
        self.svg_root.append(label.to_element())
    
    def _add_garage(self):
        """Add garage structure."""
        garage_x = 450
        garage_y = 140
        
        garage = Rectangle(
            garage_x, garage_y, GARAGE_WIDTH_SVG, GARAGE_LENGTH_SVG,
            fill=COLORS['garage_fill'],
            stroke=COLORS['garage_stroke'],
            **{'stroke-width': str(STROKE_WIDTHS['building'])}
        )
        self.svg_root.append(garage.to_element())
        
        # Add garage label
        label_x = garage_x + GARAGE_WIDTH_SVG / 2
        label_y = garage_y + GARAGE_LENGTH_SVG / 2 + 3
        label = AreaLabel.garage(label_x, label_y)
        self.svg_root.append(label.to_element())
    
    def _add_garden(self):
        """Add garden area."""
        garden_x = 400
        garden_y = 380
        
        garden = Ellipse(
            garden_x, garden_y, GARDEN_RADIUS_X_SVG, GARDEN_RADIUS_Y_SVG,
            fill=COLORS['garden_fill'],
            stroke=COLORS['garden_stroke'],
            **{'stroke-width': str(STROKE_WIDTHS['building'])}
        )
        self.svg_root.append(garden.to_element())
        
        # Add garden label
        label = AreaLabel.garden(garden_x, garden_y)
        self.svg_root.append(label.to_element())
    
    def _add_scale_info(self):
        """Add scale and metadata information."""
        scale = Label.create_dimension_text(
            100, SVG_HEIGHT - 20,
            f'{SCALE_TEXT} | Generated: 2026'
        )
        self.svg_root.append(scale.to_element())
    
    @staticmethod
    def prettify_xml(elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def save(self, filename: str = 'Ayappakkam_Layout.svg'):
        """
        Save the layout to an SVG file.
        
        Args:
            filename: Output filename (default: Ayappakkam_Layout.svg)
        """
        if self.svg_root is None:
            raise ValueError("Layout not created. Call create_layout() first.")
        
        svg_string = self.prettify_xml(self.svg_root)
        
        # Remove extra blank lines
        svg_string = '\n'.join([line for line in svg_string.split('\n') if line.strip()])
        
        # Write to file
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(svg_string)
        
        print(f'✓ Successfully created {filepath}')
        return filepath

def main():
    """Main entry point for layout generation."""
    print("Generating Ayappakkam_Layout.svg...")
    
    generator = LayoutGenerator(output_dir='output')
    generator.create_layout()
    generator.save('Ayappakkam_Layout.svg')
    
    print("✓ Layout generation complete!")

if __name__ == '__main__':
    main()
