import numpy as np
from napari_tracks_reader import napari_get_reader


# tmp_path is a pytest fixture
def test_reader_trackmate(tmp_path):
    """An example of how you might test your plugin."""

    # test the reader is callable
    my_test_file = str(tmp_path / "FakeTracks_TrackMate.xml")
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure data are read
    np.testing.assert_equal( () )
    layer_data_tuple[0].shape


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
