import xml.etree.ElementTree as ET
import numpy as np


class IcyReader:
    def __init__(self):
        super().__init__()
        self.tracks = None
        self.graph = {}

    def parse(self, tree):
        root = tree.getroot()
        self.tracks = np.empty((0, 5))

        # get the trackgroup element
        idx_trackgroup = 0
        for i in range(len(root)):
            if root[i].tag == 'trackgroup':
                idx_trackgroup = i
                break

        # parse tracks
        ids_map = {}
        self.tracks = np.empty((0, 5))
        track_id = -1
        for track_element in root[idx_trackgroup]:
            track_id += 1
            ids_map[track_element.attrib['id']] = track_id
            for detection_element in track_element:
                row = [float(track_id),
                       float(detection_element.attrib['t']),
                       float(detection_element.attrib['z']),
                       float(detection_element.attrib['y']),
                       float(detection_element.attrib['x'])
                       ]
                self.tracks = np.concatenate((self.tracks, [row]), axis=0)

        # parse linklist
        idx_linklist = 0
        for i in range(len(root)):
            if root[i].tag == 'linklist':
                idx_linklist = i
                break

        print("id map=", ids_map)
        for link_element in root[idx_linklist]:
            from_idx = ids_map[link_element.attrib['from']]
            to_idx = ids_map[link_element.attrib['to']]
            if to_idx in self.graph:
                self.graph[float(to_idx)].append(float(from_idx))
            else:
                self.graph[float(to_idx)] = [float(from_idx)]
