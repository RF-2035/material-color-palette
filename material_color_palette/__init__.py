from typing import List, Optional
from .colorspaces import RgbColor, HslColor, XyzColor, LabColor, LchColor
from .conversions import (
    hex_to_rgb, 
    rgb_to_hsl, 
    hsl_to_rgb, 
    rgb_to_xyz, 
    xyz_to_lab, 
    lab_to_lch,
    lch_to_lab,
    lab_to_xyz,
    xyz_to_rgb
)
from .palette import get_closest_golden_palette

def create_palette(color: str) -> List[str]:
    """
    Creates a Material Design color palette from a hex color string.
    """
    rgb = hex_to_rgb(color)
    
    # Logic from RgbColor.createPalette() in Kotlin
    # toHslColor().toRgbColor().toXyzColor().toLabColor().toLchColor().createPalette()
    
    hsl = rgb_to_hsl(rgb)
    rgb_normalized = hsl_to_rgb(hsl)
    xyz = rgb_to_xyz(rgb_normalized)
    lab = xyz_to_lab(xyz)
    lch = lab_to_lch(lab)
    
    golden_palette = get_closest_golden_palette(lch)
    custom_lch_palette = golden_palette.create_custom_palette(lch)
    
    rgb_palette = []
    for lch_color in custom_lch_palette:
        lab_p = lch_to_lab(lch_color)
        xyz_p = lab_to_xyz(lab_p)
        rgb_p = xyz_to_rgb(xyz_p)
        rgb_palette.append(rgb_p.rgb_hex)
        
    return rgb_palette
