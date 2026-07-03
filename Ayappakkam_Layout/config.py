#!/usr/bin/env python3
"""
Configuration settings for Ayappakkam house layout generation.
Defines colors, dimensions, fonts, and scale parameters.
"""

# ============================================================================
# SVG CANVAS SETTINGS
# ============================================================================
SVG_WIDTH = 1200
SVG_HEIGHT = 1400
SVG_PADDING = 40
SVG_VIEWBOX = f"0 0 {SVG_WIDTH} {SVG_HEIGHT}"

# ============================================================================
# COLOR PALETTE (Engineering Drawing Style)
# ============================================================================
COLORS = {
    'background': '#ffffff',
    'grid': '#e8e8e8',
    
    # Boundaries and plots
    'outer_boundary': '#000000',
    'plot_boundary': '#2e3192',
    'road': '#8b7355',
    'water': '#4dabf7',
    
    # Buildings
    'house_fill': '#fff8e1',
    'house_stroke': '#f57f17',
    'garage_fill': '#cfd8dc',
    'garage_stroke': '#455a64',
    'structure_fill': '#f0f0f0',
    'structure_stroke': '#555555',
    
    # Landscape
    'garden_fill': '#c8e6c9',
    'garden_stroke': '#558b2f',
    'landscape_fill': '#dcedc8',
    'landscape_stroke': '#689f38',
    
    # Text and annotations
    'text_primary': '#000000',
    'text_secondary': '#555555',
    'text_light': '#999999',
    'dimension_text': '#333333',
    'annotation': '#0066cc',
}

# ============================================================================
# STROKE WIDTHS (in SVG units)
# ============================================================================
STROKE_WIDTHS = {
    'outer_boundary': 2.5,
    'plot_boundary': 1.5,
    'building': 1.2,
    'dimension_line': 0.7,
    'grid': 0.3,
    'road': 1.0,
}

# ============================================================================
# FONT SIZES (in SVG units)
# ============================================================================
FONT_SIZES = {
    'title': 32,
    'subtitle': 18,
    'label_large': 16,
    'label': 14,
    'label_small': 12,
    'annotation': 10,
    'dimension': 9,
    'note': 8,
}

FONT_FAMILY = 'Arial, Helvetica, sans-serif'

# ============================================================================
# SCALE SETTINGS
# ============================================================================
SCALE_UNIT = 10  # 1 SVG unit = 10 meters in real world
SCALE_TEXT = f'1 unit = {SCALE_UNIT}m'
GRID_SPACING = 5  # Grid lines every 5 meters

# ============================================================================
# PLOT DIMENSIONS (in meters)
# ============================================================================
PLOT_OUTER_LENGTH = 120  # North-South
PLOT_OUTER_WIDTH = 80    # East-West

# Individual plot dimensions
PLOT_STANDARD_LENGTH = 20
PLOT_STANDARD_WIDTH = 15

# ============================================================================
# BUILDING DIMENSIONS (in meters)
# ============================================================================
HOUSE_LENGTH = 20
HOUSE_WIDTH = 15

GARAGE_LENGTH = 12
GARAGE_WIDTH = 8

# ============================================================================
# OFFSETS AND MARGINS
# ============================================================================
MARGIN_LEFT = 100
MARGIN_TOP = 150
MARGIN_RIGHT = 100
MARGIN_BOTTOM = 150

# ============================================================================
# LAYER DEFINITIONS
# ============================================================================
LAYERS = {
    'background': 0,
    'grid': 1,
    'boundaries': 2,
    'roads': 3,
    'structures': 4,
    'landscape': 5,
    'dimensions': 6,
    'text_labels': 7,
    'annotations': 8,
}
