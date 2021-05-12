import xml.etree.ElementTree as ET
import numpy as np


class ISBIReader:
    def __init__(self):
        super().__init__()
        self.tracks = None
        self.graph = {}

    def parse(self, tree):
        root = tree.getroot()
        self.tracks = np.empty((0, 5))

        # get the trackgroup element
        idx_trackcontest = 0
        for i in range(len(root)):
            if root[i].tag == 'TrackContestISBI2012':
                idx_trackcontest = i
                break

        # parse tracks=particles
        self.tracks = np.empty((0, 5))
        track_id = -1
        for particle_element in root[idx_trackcontest]:
            track_id += 1
            for detection_element in particle_element:
                row = [float(track_id),
                       float(detection_element.attrib['t']),
                       float(detection_element.attrib['z']),
                       float(detection_element.attrib['y']),
                       float(detection_element.attrib['x'])
                       ]
                self.tracks = np.concatenate((self.tracks, [row]), axis=0)
