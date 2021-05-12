import os
import numpy as np
from napari_tracks_reader import napari_get_reader


# tmp_path is a pytest fixture
def test_reader_trackmate(tmp_path):
    """An example of how you might test your plugin."""

    # test the reader is callable
    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'FakeTracks_TrackMate.xml')
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure data are read
    np.testing.assert_equal((200, 5), layer_data_tuple[0].shape)
    np.testing.assert_equal(8, len(layer_data_tuple[1]['graph']))


def test_reader_icy(tmp_path):
    """An example of how you might test your plugin."""

    # test the reader is callable
    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'FakeTracks_Icy.xml')
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure data are read
    np.testing.assert_equal((237, 5), layer_data_tuple[0].shape)
    np.testing.assert_equal(9, len(layer_data_tuple[1]['graph']))


def test_reader_isbi(tmp_path):
    """An example of how you might test your plugin."""

    # test the reader is callable
    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'FakeTracks_ISBI.xml')
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure data are read
    np.testing.assert_equal((156, 5), layer_data_tuple[0].shape)
    np.testing.assert_equal(0, len(layer_data_tuple[1]['graph']))


def test_reader_csv(tmp_path):
    """An example of how you might test your plugin."""

    # test the reader is callable
    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'two_tracks.csv')
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure data are read
    np.testing.assert_equal((29, 5), layer_data_tuple[0].shape)
    np.testing.assert_equal(0, len(layer_data_tuple[1]['graph']))


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
