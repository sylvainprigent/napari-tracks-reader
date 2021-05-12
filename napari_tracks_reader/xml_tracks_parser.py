import xml.etree.ElementTree as ET
from .trackmate_reader import TrackmateModelReader
from .icy_reader import IcyReader
from .isbi_reader import ISBIReader


class XmlTracksParser:
    """Load a XML file

    Load a XML file into a tree structure, identify the tracks formats and
    instantiate the format reader if found

    Parameters
    ----------
    path: str
        Path of the track XML file

    """
    def __init__(self, path):
        self._tree = ET.parse(path)
        self._root = self._tree.getroot()
        #print("root tag = ", self._root.tag)

    def parse(self):
        if self._root.tag == 'TrackMate':
            reader = TrackmateModelReader()
            reader.parse(self._tree)
            data = reader.tracks
            add_kwargs = {'graph': reader.graph}
            return data, add_kwargs
        elif self._root.tag == 'root':
            if len(self._root) >= 1:
                if self._root[0].tag == 'trackfile':
                    reader = IcyReader()
                    reader.parse(self._tree)
                    data = reader.tracks
                    add_kwargs = {'graph': reader.graph}
                    return data, add_kwargs
                elif self._root[0].tag == 'TrackContestISBI2012':
                    reader = ISBIReader()
                    reader.parse(self._tree)
                    data = reader.tracks
                    add_kwargs = {'graph': reader.graph}
                    return data, add_kwargs
        else:
            return None


