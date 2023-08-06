"""Test deprecated items."""

import pytest

import mapchete
from mapchete.errors import MapcheteProcessImportError


def test_parse_deprecated(deprecated_params):
    with mapchete.open(deprecated_params.dict) as mp:
        assert mp.config.process_bounds() == mp.config.bounds_at_zoom()
        assert mp.config.process_area() == mp.config.process_area()
        assert mp.config.at_zoom(5) == mp.config.params_at_zoom(5)
        assert mp.config.inputs == mp.config.input
        assert mp.config.crs == mp.config.process_pyramid.crs
        assert mp.config.metatiling == mp.config.process_pyramid.metatiling
        assert mp.config.pixelbuffer == mp.config.process_pyramid.pixelbuffer
        assert mp.config.process_file


def test_parse_deprecated_zooms(deprecated_params):
    deprecated_params.dict.pop("process_zoom")
    deprecated_params.dict.update(process_minzoom=0, process_maxzoom=5)
    with mapchete.open(deprecated_params.dict) as mp:
        assert mp.config.zoom_levels == list(range(0, 6))


def test_deprecated_process_class(deprecated_params):
    deprecated_params.dict.update(process_file="old_style_process.py")
    with pytest.raises(MapcheteProcessImportError):
        mapchete.open(deprecated_params.dict)


def test_deprecated_open_kwarg(mapchete_input):
    """Mapchete process as input for other process."""
    with mapchete.open(mapchete_input.path) as mp:
        config = mp.config.params_at_zoom(5)
        input_data = config["input"]["file2"]
        with pytest.raises(DeprecationWarning):
            input_data.open(next(mp.get_process_tiles(5)), resampling="bilinear")
