from ._csv_io import CSVIO
from ._trackmate_io import TrackMateIO
from ._icy_io import ICYIO
from ._isbi_io import ISBIIO
from ._st_io import StIO


def is_compatible(file_path):
    # CSV
    csv_reader = CSVIO(file_path)
    if csv_reader.is_compatible():
        return True

    # TrackMate
    trackmate_reader = TrackMateIO(file_path)
    if trackmate_reader.is_compatible():
        return True

    # ICY
    icy_reader = ICYIO(file_path)
    if icy_reader.is_compatible():
        return True

    # ISBI
    isbi_reader = ISBIIO(file_path)
    if isbi_reader.is_compatible():
        return True

    # st.json
    st_reader = StIO(file_path)
    if st_reader.is_compatible():
        return True

    return None


def read_tracks(file_path):
    """Main track reader

    This method call the first compatible reader is found

    Parameters
    ----------
    file_path: str
        Path of the track file to read

    Returns
    -------
    tracks: STracks
        Container of the trajectories

    """
    print("read tracks:", file_path)
    # CSV
    csv_reader = CSVIO(file_path)
    if csv_reader.is_compatible():
        csv_reader.read()
        return csv_reader.stracks

    # TrackMate
    trackmate_reader = TrackMateIO(file_path)
    if trackmate_reader.is_compatible():
        trackmate_reader.read()
        return trackmate_reader.stracks

    # ICY
    icy_reader = ICYIO(file_path)
    if icy_reader.is_compatible():
        print('is compatible ICY :', file_path)
        icy_reader.read()
        return icy_reader.stracks

    # ISBI
    isbi_reader = ISBIIO(file_path)
    if isbi_reader.is_compatible():
        print('is compatible ISBI :', file_path)
        isbi_reader.read()
        return isbi_reader.stracks

    #st.json
    st_reader = StIO(file_path)
    if st_reader.is_compatible():
        st_reader.read()
        return st_reader.stracks

    print('is not compatible at all :', file_path)
    return None
