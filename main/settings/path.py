from pathlib import Path


BASE_DIR = [path.parent.as_posix() for path in 
            Path(__file__).parents if path.name == 'main'][0]

RESOURCES_DIR = Path(BASE_DIR, 'main', 'resources').as_posix()

CHECK_POINTS_DIR = Path(RESOURCES_DIR, 'check_points').as_posix()

SCRIPTS_DIR = Path(RESOURCES_DIR, 'scripts').as_posix()

ICONS_DIR = Path(RESOURCES_DIR, 'icons').as_posix()

THEME_DIR = Path(RESOURCES_DIR, 'themes').as_posix()

PROJECTS_CONFIG_DIR = Path(BASE_DIR, 'projects', 'projects.json').as_posix()