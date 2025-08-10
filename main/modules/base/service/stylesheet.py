import os
import sys
import jinja2
import logging
from pathlib import Path
import platform
from xml.dom.minidom import parse
# from qt_material.resources import ResourseGenerator

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main.settings.path import THEME_DIR
TEMPLATE_FILE = Path(THEME_DIR, 'material.qss.template')


def apply_stylesheet(
    app,
    theme="",
    parent="theme",
):
    stylesheet = build_stylesheet(theme, parent)
    app.setStyleSheet(stylesheet)


# ----------------------------------------------------------------------
def build_stylesheet(
    theme="",
    parent="theme",
    template=TEMPLATE_FILE,
):

    add_fonts()
    theme = get_theme(theme)
    # set_icons_theme(theme, parent=parent)

    # Render custom template
    if os.path.exists(template):
        parent, template = os.path.split(template)
        loader = jinja2.FileSystemLoader(parent)
        env = jinja2.Environment(autoescape=False, loader=loader)
        env.filters["opacity"] = opacity
        env.filters["density"] = density
        stylesheet = env.get_template(template)

    theme.setdefault("icon", None)
    theme.setdefault("font_family", "Roboto")
    theme.setdefault("danger", "#dc3545")
    theme.setdefault("warning", "#ffc107")
    theme.setdefault("success", "#17a2b8")
    theme.setdefault("density_scale", "0")
    theme.setdefault("button_shape", "default")

    default_palette = QGuiApplication.palette()
    color = QColor(
        *[int(theme["primaryColor"][i : i + 2], 16) for i in range(1, 6, 2)] + [92]
    )
    default_palette.setColor(QPalette.ColorRole.Text, color)
    QGuiApplication.setPalette(default_palette)

    environ = {
        "linux": platform.system() == "Linux",
        "windows": platform.system() == "Windows",
        "darwin": platform.system() == "Darwin",
        'pyqt5': 'PyQt5' in sys.modules,
        "pyqt6": "PyQt6" in sys.modules,
        "pyside6": "PySide6" in sys.modules,
    }

    environ.update(theme)
    return stylesheet.render(environ)


# ----------------------------------------------------------------------
def add_fonts():
    fonts_path = Path(THEME_DIR, 'fonts')
    for font_dir in ["roboto"]:
        for font in filter(
            lambda s: s.endswith(".ttf"),
            os.listdir(os.path.join(fonts_path, font_dir)),
        ):
            QFontDatabase.addApplicationFont(os.path.join(fonts_path, font_dir, font))


# ----------------------------------------------------------------------
def get_theme(theme_name):
    theme = os.path.join(THEME_DIR, theme_name)

    document = parse(theme)
    theme = {
        child.getAttribute("name"): child.firstChild.nodeValue
        for child in document.getElementsByTagName("color")
    }

    for k in theme:
        os.environ[str(k)] = theme[k]

    for color in [
        "primaryColor",
        "primaryLightColor",
        "secondaryColor",
        "secondaryLightColor",
        "secondaryDarkColor",
        "primaryTextColor",
        "secondaryTextColor",
    ]:
        os.environ[f"QTMATERIAL_{color.upper()}"] = theme[color]
    os.environ["QTMATERIAL_THEME"] = theme_name

    return theme


# ----------------------------------------------------------------------
# def set_icons_theme(theme, parent="theme"):
#     """"""
#     source = Path(THEME_DIR, 'svgs')
#     resources = ResourseGenerator(
#         primary=theme["primaryColor"],
#         secondary=theme["secondaryColor"],
#         disabled=theme["secondaryLightColor"],
#         source=source,
#         parent=parent,
#     )
#     resources.generate()


#     QDir.addSearchPath("icon", resources.index)
#     QDir.addSearchPath(
#         "qt_material",
#         os.path.join(os.path.dirname(__file__), "resources"),
#     )


# ----------------------------------------------------------------------
def opacity(theme, value=0.5):
    r, g, b = theme[1:][0:2], theme[1:][2:4], theme[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    return f"rgba({r}, {g}, {b}, {value})"

# ----------------------------------------------------------------------
def density(value, density_scale, border=0, scale=1, density_interval=4, min_=4):
    if isinstance(value, str) and value.startswith("@"):
        return value[1:] * scale

    if value == "unset":
        return "unset"

    if isinstance(value, str):
        value = float(value.replace("px", ""))

    density = (value + (density_interval * int(density_scale)) - (border * 2)) * scale

    if density <= 0:
        density = min_
    return density