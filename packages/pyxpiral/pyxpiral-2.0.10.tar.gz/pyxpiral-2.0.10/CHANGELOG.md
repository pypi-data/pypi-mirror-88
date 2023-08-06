# Version 2.0.10
 - Fix import on unit tests

# Version 2.0.9
 - Fix default resampling filter change on pillow>=7.0.0

# Version 2.0.8
 - Fix `--scale` argument shorthand

# Version 2.0.7
 - Fix `__version__` import

# Version 2.0.6
 - Add CLI argument shorthands
 - Add `-v`, `--version` argument to print current version

# Version 2.0.5
 - Update `README.md`

# Version 2.0.4
 - Remove `__main__.py`
 - Rename `pyxpiral.py` to `__main__.py`

# Version 2.0.3
 - Add `__main__.py`

# Version 2.0.2
 - Upgrade pillow>=7.1.0 to fix several CVEs
 - Drop support for python 2

# Version 2.0.1
- Fix decode offset calculation
- Support --bg-color and --bits-color args in hex format 

# Version 2.0.0
- Improve `decode` by decoding to nearest color
- Refactor color params

# Version 1.0.0
- Use `PIL.Image` as `Pyxpiral.decode` input parameter instead of image file handler or image filename.
- Fix image mode detection on linux systems.
- Add Dockerfile python2 and python3 alpine linux based project environment definitions

# Version 0.0.3
- Fix write modifier for default output file.

# Version 0.0.2
- Fix terminator bit on gif sequence.

# Version 0.0.1
- First public release.
