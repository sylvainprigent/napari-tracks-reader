import numpy as np
from napari_tracks_reader import napari_get_reader


# tmp_path is a pytest fixture
def test_reader(tmp_path):
    """An example of how you might test your plugin."""

    # write some fake data using your supported file format
    my_test_file = str(tmp_path / "FakeTracks_split_merge.xml")

    # try to read it back in
    reader = napari_get_reader(my_test_file)
    assert callable(reader)


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
