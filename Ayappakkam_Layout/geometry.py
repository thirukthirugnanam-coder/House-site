#!/usr/bin/env python3
"""
Core SVG geometry engine for creating vector-based drawing elements.
Provides classes for shapes, paths, and geometric primitives.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

@dataclass
class Point:
    """Represents a 2D point."""
    x: float
    y: float
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def offset(self, dx: float, dy: float) -> 'Point':
        """Return a new point offset by dx, dy."""
        return Point(self.x + dx, self.y + dy)

class SVGElement:
    """Base class for all SVG elements."""
    
    def __init__(self, tag: str, **kwargs):
        """Initialize SVG element with tag and attributes."""
        self.tag = tag
        self.attributes = {k: str(v) for k, v in kwargs.items()}
        self.children: List[SVGElement] = []
        self.text_content = None
    
    def set_attr(self, key: str, value: Any) -> 'SVGElement':
        """Set an attribute and return self for chaining."""
        self.attributes[key] = str(value)
        return self
    
    def add_class(self, classname: str) -> 'SVGElement':
        """Add a CSS class."""
        current = self.attributes.get('class', '')
        self.attributes['class'] = (current + ' ' + classname).strip()
        return self
    
    def add_child(self, child: 'SVGElement') -> 'SVGElement':
        """Add a child element and return self for chaining."""
        self.children.append(child)
        return self
    
    def set_text(self, text: str) -> 'SVGElement':
        """Set text content and return self."""
        self.text_content = text
        return self
    
    def to_element(self) -> ET.Element:
        """Convert to ElementTree element."""
        elem = ET.Element(self.tag, self.attributes)
        if self.text_content:
            elem.text = self.text_content
        for child in self.children:
            elem.append(child.to_element())
        return elem

# ============================================================================
# SHAPE CLASSES
# ============================================================================

class Rectangle(SVGElement):
    """Rectangle shape."""
    
    def __init__(self, x: float, y: float, width: float, height: float, **kwargs):
        super().__init__('rect', x=x, y=y, width=width, height=height, **kwargs)

class Circle(SVGElement):
    """Circle shape."""
    
    def __init__(self, cx: float, cy: float, r: float, **kwargs):
        super().__init__('circle', cx=cx, cy=cy, r=r, **kwargs)

class Ellipse(SVGElement):
    """Ellipse shape."""
    
    def __init__(self, cx: float, cy: float, rx: float, ry: float, **kwargs):
        super().__init__('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)

class Line(SVGElement):
    """Line segment."""
    
    def __init__(self, x1: float, y1: float, x2: float, y2: float, **kwargs):
        super().__init__('line', x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)

class Polyline(SVGElement):
    """Polyline (connected line segments)."""
    
    def __init__(self, points: List[Tuple[float, float]], **kwargs):
        points_str = ' '.join(f'{x},{y}' for x, y in points)
        super().__init__('polyline', points=points_str, **kwargs)

class Polygon(SVGElement):
    """Polygon (closed polyline)."""
    
    def __init__(self, points: List[Tuple[float, float]], **kwargs):
        points_str = ' '.join(f'{x},{y}' for x, y in points)
        super().__init__('polygon', points=points_str, **kwargs)

class Path(SVGElement):
    """SVG path element for complex shapes."""
    
    def __init__(self, d: str, **kwargs):
        super().__init__('path', d=d, **kwargs)
    
    @staticmethod
    def move_to(x: float, y: float) -> str:
        """Move to command."""
        return f'M {x} {y}'
    
    @staticmethod
    def line_to(x: float, y: float) -> str:
        """Line to command."""
        return f'L {x} {y}'
    
    @staticmethod
    def horizontal_line_to(x: float) -> str:
        """Horizontal line to command."""
        return f'H {x}'
    
    @staticmethod
    def vertical_line_to(y: float) -> str:
        """Vertical line to command."""
        return f'V {y}'
    
    @staticmethod
    def close_path() -> str:
        """Close path command."""
        return 'Z'

class Text(SVGElement):
    """Text element."""
    
    def __init__(self, x: float, y: float, content: str = '', **kwargs):
        super().__init__('text', x=x, y=y, **kwargs)
        self.text_content = content

class Group(SVGElement):
    """Group element for organizing related elements."""
    
    def __init__(self, **kwargs):
        super().__init__('g', **kwargs)

class Defs(SVGElement):
    """Definitions element for reusable patterns and styles."""
    
    def __init__(self):
        super().__init__('defs')

class Style(SVGElement):
    """Style element for CSS."""
    
    def __init__(self, css: str = ''):
        super().__init__('style')
        self.text_content = css

class Marker(SVGElement):
    """Marker element for arrow heads and line ends."""
    
    def __init__(self, marker_id: str, **kwargs):
        super().__init__('marker', id=marker_id, **kwargs)

# ============================================================================
# SVG DOCUMENT ROOT
# ============================================================================

class SVGDocument:
    """Main SVG document."""
    
    def __init__(self, width: float, height: float, viewbox: str = None):
        self.width = width
        self.height = height
        self.viewbox = viewbox or f'0 0 {width} {height}'
        self.root = SVGElement('svg',
            xmlns='http://www.w3.org/2000/svg',
            width=width,
            height=height,
            viewBox=self.viewbox
        )
        self.defs = Defs()
        self.root.add_child(self.defs)
    
    def add_element(self, element: SVGElement) -> SVGDocument:
        """Add element to document and return self for chaining."""
        self.root.add_child(element)
        return self
    
    def add_defs(self, element: SVGElement) -> SVGDocument:
        """Add element to defs section."""
        self.defs.add_child(element)
        return self
    
    def add_style(self, css: str) -> SVGDocument:
        """Add CSS style to document."""
        style = Style(css)
        self.add_defs(style)
        return self
    
    def to_element(self) -> ET.Element:
        """Convert to ElementTree element."""
        return self.root.to_element()
    
    def to_string(self) -> str:
        """Convert to XML string."""
        elem = self.to_element()
        return ET.tostring(elem, encoding='unicode')

# ============================================================================
# GEOMETRY UTILITIES
# ============================================================================

class GeometryUtils:
    """Utility functions for geometric calculations."""
    
    @staticmethod
    def distance(p1: Point, p2: Point) -> float:
        """Calculate distance between two points."""
        return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
    
    @staticmethod
    def midpoint(p1: Point, p2: Point) -> Point:
        """Calculate midpoint between two points."""
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    
    @staticmethod
    def rotate_point(point: Point, center: Point, angle_degrees: float) -> Point:
        """Rotate a point around a center by angle in degrees."""
        import math
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        dx = point.x - center.x
        dy = point.y - center.y
        
        new_x = center.x + (dx * cos_a - dy * sin_a)
        new_y = center.y + (dx * sin_a + dy * cos_a)
        
        return Point(new_x, new_y)
    
    @staticmethod
    def offset_line(p1: Point, p2: Point, offset: float) -> Tuple[Point, Point]:
        """Create parallel line offset by specified distance."""
        import math
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist == 0:
            return p1, p2
        
        px = -dy / dist * offset
        py = dx / dist * offset
        
        return (Point(p1.x + px, p1.y + py),
                Point(p2.x + px, p2.y + py))
