#!/usr/bin/env python3
"""
Dimension calculations, unit conversions, and coordinate management.
Handles real-world to SVG coordinate transformations.
"""

from config import SCALE_UNIT
from typing import Tuple

class Dimensions:
    """Handle dimension conversions between real-world and SVG units."""
    
    def __init__(self, scale_unit: float = SCALE_UNIT):
        """
        Initialize dimensions handler.
        
        Args:
            scale_unit: Real-world meters per SVG unit (default from config)
        """
        self.scale_unit = scale_unit
    
    def meters_to_svg(self, meters: float) -> float:
        """Convert real-world meters to SVG units."""
        return meters / self.scale_unit
    
    def svg_to_meters(self, svg_units: float) -> float:
        """Convert SVG units to real-world meters."""
        return svg_units * self.scale_unit
    
    def get_dimensions_svg(self, width_m: float, height_m: float) -> Tuple[float, float]:
        """
        Get dimensions in SVG units.
        
        Args:
            width_m: Width in meters
            height_m: Height in meters
            
        Returns:
            Tuple of (width_svg, height_svg)
        """
        return (
            self.meters_to_svg(width_m),
            self.meters_to_svg(height_m)
        )

class CoordinateSystem:
    """Manage coordinate system transformations and canvas positioning."""
    
    def __init__(self, origin_x: float, origin_y: float, scale_unit: float = SCALE_UNIT):
        """
        Initialize coordinate system.
        
        Args:
            origin_x: SVG X coordinate of origin
            origin_y: SVG Y coordinate of origin
            scale_unit: Meters per SVG unit
        """
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.dimensions = Dimensions(scale_unit)
    
    def to_svg_coords(self, real_x: float, real_y: float) -> Tuple[float, float]:
        """
        Convert real-world coordinates to SVG coordinates.
        
        Args:
            real_x: X position in meters
            real_y: Y position in meters
            
        Returns:
            Tuple of (svg_x, svg_y)
        """
        svg_x = self.origin_x + self.dimensions.meters_to_svg(real_x)
        svg_y = self.origin_y + self.dimensions.meters_to_svg(real_y)
        return (svg_x, svg_y)
    
    def to_real_coords(self, svg_x: float, svg_y: float) -> Tuple[float, float]:
        """
        Convert SVG coordinates to real-world coordinates.
        
        Args:
            svg_x: X position in SVG units
            svg_y: Y position in SVG units
            
        Returns:
            Tuple of (real_x, real_y) in meters
        """
        real_x = self.dimensions.svg_to_meters(svg_x - self.origin_x)
        real_y = self.dimensions.svg_to_meters(svg_y - self.origin_y)
        return (real_x, real_y)

class BoundingBox:
    """Represents a rectangular bounding box."""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialize bounding box.
        
        Args:
            x: Top-left X coordinate
            y: Top-left Y coordinate
            width: Box width
            height: Box height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @property
    def x1(self) -> float:
        """Left edge."""
        return self.x
    
    @property
    def y1(self) -> float:
        """Top edge."""
        return self.y
    
    @property
    def x2(self) -> float:
        """Right edge."""
        return self.x + self.width
    
    @property
    def y2(self) -> float:
        """Bottom edge."""
        return self.y + self.height
    
    @property
    def center_x(self) -> float:
        """Horizontal center."""
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        """Vertical center."""
        return self.y + self.height / 2
    
    def contains(self, x: float, y: float) -> bool:
        """Check if point is inside bounding box."""
        return (self.x1 <= x <= self.x2 and 
                self.y1 <= y <= self.y2)
    
    def expand(self, padding: float) -> 'BoundingBox':
        """Return new box expanded by padding."""
        return BoundingBox(
            self.x - padding,
            self.y - padding,
            self.width + 2 * padding,
            self.height + 2 * padding
        )

# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

# Default dimensions converter
dims = Dimensions()

# Pre-calculated conversions for common values
CONVERSIONS = {
    1: dims.meters_to_svg(1),
    5: dims.meters_to_svg(5),
    10: dims.meters_to_svg(10),
    15: dims.meters_to_svg(15),
    20: dims.meters_to_svg(20),
    40: dims.meters_to_svg(40),
    60: dims.meters_to_svg(60),
    80: dims.meters_to_svg(80),
    120: dims.meters_to_svg(120),
}
