import xml.etree.ElementTree as ET
import numpy as np


def read_trackmate(file):
    reader = TrackmateModelReader()
    reader.read(file)
    return reader.tracks


class TrackmateModelReader():
    def __init__(self):
        super().__init__()
        self.file = ''
        self.root = None
        self.tracks = None

    def read(self, file):
        self.file = file

        tree = ET.parse(self.file)
        self.root = tree.getroot()
        self.tracks = np.empty((0, 5))

        # get filtered tracks
        for filtered_track in self.root[0][3]:
            # get the edges of each filtered tracks
            track_id = int(filtered_track.attrib['TRACK_ID'])
            for all_track in self.root[0][2]:
                if int(all_track.attrib['TRACK_ID']) == track_id:
                    self.parse_track(track_id, all_track)
        self.tracks = np.unique(self.tracks, axis=0)

    def parse_track(self, track_id, xml_element):
        for child in xml_element:
            source_pos = self.find_edge_position(track_id,
                                                 child.attrib['SPOT_SOURCE_ID'])
            target_pos = self.find_edge_position(track_id,
                                                 child.attrib['SPOT_TARGET_ID'])
            self.tracks = np.concatenate((self.tracks, [source_pos],
                                          [target_pos]), axis=0)

    def find_edge_position(self, track_id, spot_id):
        all_spots = self.root[0][1]
        for spot_in_frame in all_spots:
            for spot in spot_in_frame:
                if spot.attrib['ID'] == spot_id:
                    return [float(track_id),
                            float(spot.attrib['POSITION_T']),
                            float(spot.attrib['POSITION_Z']),
                            float(spot.attrib['POSITION_Y']),
                            float(spot.attrib['POSITION_X'])]