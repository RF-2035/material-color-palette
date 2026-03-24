from dataclasses import dataclass
from math import sqrt, pow, sin, cos, exp, radians, atan2, degrees, floor

def kotlin_round(val: float) -> int:
    """Matches Kotlin's Math.round() behavior for Double."""
    return floor(val + 0.5)

@dataclass(frozen=True)
class RgbColor:
    red: float
    green: float
    blue: float
    alpha: float = 1.0

    @property
    def rgb_hex(self) -> str:
        return f"{kotlin_round(self.red * 0xff):02X}{kotlin_round(self.green * 0xff):02X}{kotlin_round(self.blue * 0xff):02X}"

    @property
    def rgba_hex(self) -> str:
        return f"{kotlin_round(self.red * 0xff):02X}{kotlin_round(self.green * 0xff):02X}{kotlin_round(self.blue * 0xff):02X}{kotlin_round(self.alpha * 0xff):02X}"

    @property
    def argb_hex(self) -> str:
        return f"{kotlin_round(self.alpha * 0xff):02X}{kotlin_round(self.red * 0xff):02X}{kotlin_round(self.green * 0xff):02X}{kotlin_round(self.blue * 0xff):02X}"

    @property
    def rgb(self) -> int:
        return (kotlin_round(self.red * 0xff) << 16) | (kotlin_round(self.green * 0xff) << 8) | kotlin_round(self.blue * 0xff)

    @property
    def rgba(self) -> int:
        return (kotlin_round(self.red * 0xff) << 24) | (kotlin_round(self.green * 0xff) << 16) | (kotlin_round(self.blue * 0xff) << 8) | kotlin_round(self.alpha * 0xff)

    @property
    def argb(self) -> int:
        return (kotlin_round(self.alpha * 0xff) << 24) | (kotlin_round(self.red * 0xff) << 16) | (kotlin_round(self.green * 0xff) << 8) | kotlin_round(self.blue * 0xff)

@dataclass(frozen=True)
class HslColor:
    hue: int
    saturation: float
    lightness: float
    alpha: float = 1.0

@dataclass(frozen=True)
class XyzColor:
    x: float
    y: float
    z: float
    alpha: float = 1.0

@dataclass(frozen=True)
class LabColor:
    lightness: float
    a: float
    b: float
    alpha: float = 1.0

@dataclass(frozen=True)
class LchColor:
    lightness: float
    chroma: float
    hue: float
    alpha: float = 1.0

    def delta_e(self, other: 'LchColor') -> float:
        delta_lightness = self.lightness - other.lightness
        mean_lightness = (self.lightness + other.lightness) / 2.0
        mean_chroma = (self.chroma + other.chroma) / 2.0

        a_factor = 1 - sqrt(pow(mean_chroma, 7) / (pow(mean_chroma, 7) + pow(25.0, 7)))
        
        from .conversions import lch_to_lab, lab_to_lch
        
        lab_self = lch_to_lab(self)
        this_prime = lab_to_lch(LabColor(lab_self.lightness, lab_self.a + lab_self.a / 2.0 * a_factor, lab_self.b, self.alpha))
        
        lab_other = lch_to_lab(other)
        other_prime = lab_to_lch(LabColor(lab_other.lightness, lab_other.a + lab_other.a / 2.0 * a_factor, lab_other.b, other.alpha))

        delta_chroma_prime = this_prime.chroma - other_prime.chroma
        mean_chroma_prime = (this_prime.chroma + other_prime.chroma) / 2.0

        delta_hue_prime = self._hue_delta(this_prime, other_prime)
        delta_h_prime = 2.0 * sqrt(this_prime.chroma * other_prime.chroma) * sin(radians(delta_hue_prime / 2.0))
        mean_hue_prime = self._mean_hue(this_prime, other_prime)

        t = 1.0 - \
            .17 * cos(radians(mean_hue_prime - 30.0)) + \
            .24 * cos(radians(2.0 * mean_hue_prime)) + \
            .32 * cos(radians(3.0 * mean_hue_prime + 6.0)) - \
            .2 * cos(radians(4.0 * mean_hue_prime - 63.0))
        
        sl = 1.0 + .015 * pow(mean_lightness - 50.0, 2) / sqrt(20.0 + pow(mean_lightness - 50.0, 2))
        sc = 1.0 + .045 * mean_chroma_prime
        sh = 1.0 + .015 * mean_chroma_prime * t
        rt = -2.0 * sqrt(pow(mean_chroma_prime, 7) / (pow(mean_chroma_prime, 7) + pow(25.0, 7))) * \
             sin(radians(60.0 * exp(-pow((mean_hue_prime - 275.0) / 25.0, 2))))

        return sqrt(
            pow(delta_lightness / sl, 2) +
            pow(delta_chroma_prime / sc, 2) +
            pow(delta_h_prime / sh, 2) +
            rt * (delta_chroma_prime / sc) * (delta_h_prime / sh)
        )

    @staticmethod
    def _hue_delta(this: 'LchColor', other: 'LchColor') -> float:
        if -180.0 <= (this.hue - other.hue) <= 180.0:
            return this.hue - other.hue
        elif this.hue <= other.hue:
            return this.hue - other.hue + 360.0
        else:
            return this.hue - other.hue - 360.0

    @staticmethod
    def _mean_hue(this: 'LchColor', other: 'LchColor') -> float:
        if -180.0 <= (this.hue - other.hue) <= 180.0:
            return (other.hue + this.hue) / 2.0
        elif other.hue + this.hue < 360.0:
            return (other.hue + this.hue + 360.0) / 2.0
        else:
            return (other.hue + this.hue - 360.0) / 2.0
