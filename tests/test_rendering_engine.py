import os
from pathlib import Path

from magrathea.rendering_engine import render_map_to_buffer, render_map_to_png


def test_render_png(tmp_path: Path) -> None:
    d = tmp_path / "output"
    d.mkdir()
    filename = d / "test_output.png"

    render_map_to_png(64, 2, str(filename))

    assert os.path.exists(filename), "PNG file should be created"


def test_render_buffer() -> None:
    buf = render_map_to_buffer(64, 2)
    assert buf.getbuffer().nbytes > 0, "Buffer should contain data"
    buf.close()
