# KitchenArt DRF Utilities

This package contains helpers and utilities used at 
KitchenArt for django-based projects.

Features:
- Base Class Model for timestamped and soft delete.
- Serializer classes for timestamped.
- View classes for soft delete.
- Log Activity module
- Basic publisher classes
- Translation serializer classes
- Helper parse identity from href
- Custom drf exception handler

## Installation

```shell
pip install ka-drf-utils

# or, if you'd like to use broker and translation
pip install ka-drf-utils[broker,translation]
```