# Copyright 2020 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Handle loading, storing, saving, and default values for program settings.
"""

import os
import io
import logging
import atexit

import tomlkit
import appdirs


def set_defaults():
    update(tomlkit.parse(
"""
[alignment]

[alignment.ui]
cameraindex = 0
auto = false

[[alignment.ui.rois]]
pos = [600, 300]
size = [75, 75]
angle = 0

[[alignment.ui.rois]]
pos = [700, 400]
size = [75, 75]
angle = 0

[rawdata]

[rawdata.crosshair]
# An RGBA colour for the crosshairs
colour = [0, 255, 0, 255]
# An RGBA colur for the crosshairs when highlighted
highlight = [255, 0, 0, 255]

[rawdata.scangradient]
# Gradient start and stop RGBA colours to use for individual scan traces
start = [0, 64, 255, 128]
stop  = [192, 0, 0, 128]
# Highlight RGBA colour to use when highlighting a specific scan trace
highlight = [192, 192, 192, 255]

[directories]
data = ""

[hardware]

# Whether to search for and initialise hardware devices.
# If set to false (the default), no hardware detection will take place.
# The software will still be usable for data visualisation and analysis.
init_hardware = false

# Alignment camera list
# Each entry specifies an alignment camera
#   name (string) : Friendly name for the camera to use in the application
#   filter (string) : Regular expression to match the camera device name, eg. "Logitech"
#   id (int) : If multiple devices match the filter, index of the match
#   focus (int) : Fixed focus point, ranging from 0 (infinity) to 51 (macro).
[[hardware.aligncams]]
name = "Alignment 1"
filter = ""
index = 0
focus = 49
"""
    ))
    # Set default directories
    if not data["directories"]["data"]:
        data["directories"]["data"] = os.path.expanduser("~")


def read(reset=False):
    global data
    newconfig = tomlkit.toml_document.TOMLDocument() if reset else data.copy()
    try:
        with io.open(configfile, encoding="utf-8") as f:
            _update_dict(newconfig, tomlkit.loads(f.read()))
    except:
        log.exception(f"Error reading configuration from file {configfile}")
        return
    data = newconfig


def write():
    try:
        with io.open(configfile, "w", encoding="utf-8") as f:
            f.write(data.as_string())
    except:
        log.exception(f"Error writing configuration to file {configfile}")


def update(newdict):
    _update_dict(data, newdict)


def _update_dict(olddict, newdict):
    """Recursively update dicts."""
    for k, _ in newdict.items():
        if k in olddict and isinstance(olddict[k], dict) and isinstance(newdict[k], dict):
            _update_dict(olddict[k], newdict[k])
        else:
            olddict[k] = newdict[k]


# Module init ##################################################################

log = logging.getLogger(__name__)

configfile = os.path.join(appdirs.user_config_dir("trspectrometer", False), "trspectrometer.toml")
log.info(f"Configuration file location is {configfile}")

# Start with empty TOMLDocument, add defaults, then load/overwrite from file
data = tomlkit.toml_document.TOMLDocument()
set_defaults()
if not os.access(configfile, os.F_OK):
    # Create new file
    log.info("Configuration file doesn't exist, creating default")
    try:
        os.mkdir(os.path.dirname(configfile))
    except FileExistsError:
        pass
    except:
        log.exception(f"Unable to create directory for configuration at {os.path.dirname(configfile)}")
        pass
    write()
read(reset=False)

# Save back out to disk when application shuts down
atexit.register(write)
