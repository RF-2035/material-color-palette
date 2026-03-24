from math import pow, sqrt, atan2, degrees, radians, cos, sin
from .colorspaces import RgbColor, HslColor, XyzColor, LabColor, LchColor, kotlin_round

def rgb_to_hsl(rgb: RgbColor) -> HslColor:
    max_val = max(rgb.red, rgb.green, rgb.blue)
    min_val = min(rgb.red, rgb.green, rgb.blue)
    delta = max_val - min_val
    
    if delta == 0.0:
        hue = 0.0
    elif max_val == rgb.red:
        hue = 60.0 * ((rgb.green - rgb.blue) / delta)
    elif max_val == rgb.green:
        hue = 60.0 * ((rgb.blue - rgb.red) / delta + 2)
    else:
        hue = 60.0 * ((rgb.red - rgb.green) / delta + 4)
    
    hue = (hue + 360.0) % 360.0
    
    if max_val == 0.0 or min_val == 1.0:
        saturation = 0.0
    else:
        saturation = delta / (1 - abs(max_val + min_val - 1))
    
    lightness = (max_val + min_val) / 2.0
    
    return HslColor(kotlin_round(hue), saturation, lightness, rgb.alpha)

def hsl_to_rgb(hsl: HslColor) -> RgbColor:
    chroma = (1 - abs(2.0 * hsl.lightness - 1.0)) * hsl.saturation
    hue_prime = hsl.hue / 60.0
    x = chroma * (1 - abs(hue_prime % 2 - 1))
    m = hsl.lightness - chroma / 2.0

    if hue_prime < 1.0:
        return RgbColor(chroma + m, x + m, m, hsl.alpha)
    elif hue_prime < 2.0:
        return RgbColor(x + m, chroma + m, m, hsl.alpha)
    elif hue_prime < 3.0:
        return RgbColor(m, chroma + m, x + m, hsl.alpha)
    elif hue_prime < 4.0:
        return RgbColor(m, x + m, chroma + m, hsl.alpha)
    elif hue_prime < 5.0:
        return RgbColor(x + m, m, chroma + m, hsl.alpha)
    else:
        return RgbColor(chroma + m, m, x + m, hsl.alpha)

def _correct_gamma(value: float) -> float:
    return value / 12.92 if value <= 0.04045 else pow((value + 0.055) / 1.055, 2.4)

def rgb_to_xyz(rgb: RgbColor) -> XyzColor:
    r = _correct_gamma(rgb.red)
    g = _correct_gamma(rgb.green)
    b = _correct_gamma(rgb.blue)
    
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    
    return XyzColor(x, y, z, rgb.alpha)

def _f(value: float) -> float:
    delta = 6.0 / 29.0
    return pow(value, 1.0 / 3.0) if value > pow(delta, 3) else value / (3.0 * pow(delta, 2)) + 4.0 / 29.0

def xyz_to_lab(xyz: XyzColor) -> LabColor:
    fx = _f(xyz.x / 0.95047)
    fy = _f(xyz.y)
    fz = _f(xyz.z / 1.08883)
    
    lightness = 116.0 * fy - 16
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    
    return LabColor(lightness, a, b, xyz.alpha)

def lab_to_lch(lab: LabColor) -> LchColor:
    lightness = lab.lightness
    chroma = sqrt(pow(lab.a, 2) + pow(lab.b, 2))
    if 1E-4 > abs(lab.b) and 1E-4 > abs(lab.a):
        hue = 0.0
    else:
        hue = (degrees(atan2(lab.b, lab.a)) + 360.0) % 360.0
    
    return LchColor(lightness, chroma, hue, lab.alpha)

def lch_to_lab(lch: LchColor) -> LabColor:
    return LabColor(
        lightness=lch.lightness,
        a=lch.chroma * cos(radians(lch.hue)),
        b=lch.chroma * sin(radians(lch.hue)),
        alpha=lch.alpha
    )

def _f_inv(value: float) -> float:
    delta = 6.0 / 29.0
    return pow(value, 3) if value > delta else 3.0 * pow(delta, 2) * (value - 4.0 / 29.0)

def lab_to_xyz(lab: LabColor) -> XyzColor:
    fy = (lab.lightness + 16.0) / 116.0
    fx = fy + lab.a / 500.0
    fz = fy - lab.b / 200.0
    
    x = 0.95047 * _f_inv(fx)
    y = 1.0 * _f_inv(fy)
    z = 1.08883 * _f_inv(fz)
    
    return XyzColor(x, y, z, lab.alpha)

def _reverse_gamma_correction(value: float) -> float:
    return 12.92 * value if value <= 0.0031308 else 1.055 * pow(value, 1.0 / 2.4) - 0.055

def xyz_to_rgb(xyz: XyzColor) -> RgbColor:
    r = _reverse_gamma_correction(3.2404542 * xyz.x + -1.5371385 * xyz.y + -0.4985314 * xyz.z)
    g = _reverse_gamma_correction(-0.9692660 * xyz.x + 1.8760108 * xyz.y + 0.0415560 * xyz.z)
    b = _reverse_gamma_correction(0.0556434 * xyz.x + -0.2040259 * xyz.y + 1.0572252 * xyz.z)
    
    return RgbColor(
        max(0.0, min(1.0, r)),
        max(0.0, min(1.0, g)),
        max(0.0, min(1.0, b)),
        xyz.alpha
    )

def hex_to_rgb(hex_str: str) -> RgbColor:
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 8:
        val = int(hex_str, 16)
        return RgbColor(
            ((val >> 24) & 0xff) / 255.0,
            ((val >> 16) & 0xff) / 255.0,
            ((val >> 8) & 0xff) / 255.0,
            (val & 0xff) / 255.0
        )
    elif len(hex_str) == 6:
        val = int(hex_str, 16)
        return RgbColor(
            ((val >> 16) & 0xff) / 255.0,
            ((val >> 8) & 0xff) / 255.0,
            (val & 0xff) / 255.0
        )
    else:
        raise ValueError("Invalid hex color string length")
