import xml.etree.ElementTree as ET
import numpy as np


class TrackmateModelReader:
    def __init__(self):
        super().__init__()
        self.file = ''
        self.tracks = None
        self.graph = {}

        self._root = None
        self._model_idx = 0
        self._track_ids_count = -1
        self._starting_sources = []
        self._starting_track_idx = []

    def read(self, file):
        self.file = file

        tree = ET.parse(self.file)
        self._root = tree.getroot()
        self.tracks = np.empty((0, 5))

        for i in range(len(self._root)):
            if self._root[i].tag == 'Model':
                self._model_idx = i
                break

        for filtered_track in self._root[self._model_idx][3]:
            # get the edges of each filtered tracks
            track_id = int(filtered_track.attrib['TRACK_ID'])
            for all_track in self._root[self._model_idx][2]:
                if int(all_track.attrib['TRACK_ID']) == track_id:
                    # if track_id == 0:  # remove later
                    self.get_track_edges(track_id, all_track)

    def get_track_edges(self, track_id, xml_element):
        sources = []
        targets = []
        for child in xml_element:
            source_spot = self.find_spot(child.attrib['SPOT_SOURCE_ID'])
            target_spot = self.find_spot(child.attrib['SPOT_TARGET_ID'])
            sources.append(source_spot)
            targets.append(target_spot)

        sources = np.array(sources)
        targets = np.array(targets)

        # sort sources and targets
        sort_idxs = sources[:, 1].argsort()
        sources = sources[sort_idxs]
        targets = targets[sort_idxs]

        # search for splits ids
        unique, counts = np.unique(sources[:, 0], return_counts=True)
        split_idxs = unique[np.where(counts > 1)]

        # search merge ids
        uniquet, countst = np.unique(targets[:, 0], return_counts=True)
        merge_idxs = uniquet[np.where(countst > 1)]

        self._track_ids_count += 1
        self.extract_subtrack(sources, targets, split_idxs, merge_idxs,
                              sources[0, 0], self._track_ids_count)

    def extract_subtrack(self, sources, targets, split_idxs, merge_idxs,
                         source_id, track_id):

        self._starting_sources.append(source_id)
        self._starting_track_idx.append(track_id)
        idx = np.where(sources[:, 0] == source_id)[0][0]

        # create new track
        # add sources
        source = sources[idx, :].copy()

        source[0] = track_id
        self.tracks = np.concatenate((self.tracks, [source]), axis=0)
        # add next targets
        while 1:
            source = sources[idx, :].copy()
            target = targets[idx, :].copy()
            if source[0] in split_idxs:
                # maybe need to start in the next point
                split_sources = np.where(sources[:, 0] == source[0])[0]
                for ss_id in split_sources:
                    self._track_ids_count += 1
                    next_track_id = self._track_ids_count
                    self.graph[next_track_id] = track_id
                    next_idx = targets[ss_id, 0].copy()
                    self.extract_subtrack(sources, targets, split_idxs,
                                          merge_idxs, next_idx, next_track_id)
                break
            elif target[0] in merge_idxs:
                starting_points = np.where(sources[:, 0] == target[0])
                for sp_idx in starting_points[0]:
                    if sources[sp_idx, 0] not in self._starting_sources:
                        self._track_ids_count += 1
                        next_track_id = self._track_ids_count
                        self.graph[next_track_id] = [track_id]

                        self.extract_subtrack(sources, targets, split_idxs,
                                              merge_idxs, sources[sp_idx, 0],
                                              next_track_id)
                    else:
                        ind = self._starting_sources.index(sources[sp_idx, 0])
                        merge_id = self._starting_track_idx[ind]
                        if merge_id in self.graph:
                            self.graph[merge_id].append(track_id)
                        else:
                            self.graph[merge_id] = [track_id]
                break
            else:
                target[0] = track_id
                self.tracks = np.concatenate((self.tracks, [target]), axis=0)

            # go to the next
            idx = np.where(sources[:, 0] == targets[idx, 0])[0]
            if len(idx) > 0:
                idx = idx[0]
            else:
                break

    def find_spot(self, spot_id):
        all_spots = self._root[self._model_idx][1]
        for spot_in_frame in all_spots:
            for spot in spot_in_frame:
                if spot.attrib['ID'] == spot_id:
                    return [int(spot_id),
                            float(spot.attrib['POSITION_T']),
                            float(spot.attrib['POSITION_Z']),
                            float(spot.attrib['POSITION_Y']),
                            float(spot.attrib['POSITION_X'])]