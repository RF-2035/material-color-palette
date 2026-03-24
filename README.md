# Material Design Color Palette Generator

A reverse engineered library for generating a custom Material Design color palette, [Hammwerk/material-color-palette](https://github.com/Hammwerk/material-color-palette "Hammwerk/material-color-palette"), ported to Python. The original tool can be
seen [here](https://material.io/design/color/the-color-system.html#tools-for-picking-colors "Google's palette generation tool")

![Example palettes](example-palettes.png "Example palettes")

## Color Palette Generation

The algorithm to generate a Material Design color palette is ported from the original Kotlin implementation. It is exactly the same as the algorithm that is used in [Google's palette generation tool](
https://material.io/design/color/the-color-system.html#tools-for-picking-colors "Google's palette generation tool").

## Usage

```python
from material_color_palette import create_palette

custom_palette = create_palette("F44336")
print(custom_palette)
```

produces the following color palette:

![Red palette](red-palette.png "Red palette")

```python
[
    "FFEBEE",
    "FFCDD2",
    "EF9A9A",
    "E57373",
    "EF5350",
    "F44336",
    "E53935",
    "D32F2F",
    "C62828",
    "B71B1C"
]
```

## Installation

You can install this package locally:

```bash
pip install .
```

## Development

Run tests using pytest:

```bash
pytest
```

## License
    MIT License

    Copyright (c) 2021 David Hamm
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
