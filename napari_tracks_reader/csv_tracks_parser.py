import numpy as np
import pandas as pd


class CsvTracksParser:
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.tracks = None
        self.graph = {}

    def parse(self):
        df = pd.read_csv(self.path)
        headers = list(df.columns.values)
        in_tracks = df.to_numpy()

        self.tracks = np.zeros((in_tracks.shape[0], 5))
        if 'TrackID' in headers:
            index = headers.index('TrackID')
            self.tracks[:, 0] = in_tracks[:, index]
        if 't' in headers:
            index = headers.index('t')
            self.tracks[:, 1] = in_tracks[:, index]
        if 'z' in headers:
            index = headers.index('z')
            self.tracks[:, 2] = in_tracks[:, index]
        if 'y' in headers:
            index = headers.index('y')
            self.tracks[:, 3] = in_tracks[:, index]
        if 'x' in headers:
            index = headers.index('x')
            self.tracks[:, 4] = in_tracks[:, index]

        return self.tracks, {'graph': {}}
        # TODO: parse attributes
