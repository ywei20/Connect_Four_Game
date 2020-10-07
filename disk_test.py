from disk import Disk

params = {
    "SPACE": {'w': 700, 'h': 700},
    "rows": 6,
    "col_idx": 3,
    "disks_of_col": 1,
    "isRed": 1,
    "diam": 100
}


def test_constructor():
    d = Disk(params["SPACE"], params["rows"], params["col_idx"],
             params["disks_of_col"], params["isRed"], params["diam"])

    assert d.SPACE['w'] == params["SPACE"]['w'] and \
        d.SPACE['h'] == params["SPACE"]['h'] and \
        d.diam == params["diam"] and \
        d.isRed == params["isRed"] and \
        d.disks_of_col == params["disks_of_col"] and \
        hasattr(d, "y_vel") and \
        hasattr(d, "g") and \
        hasattr(d, "fill_color") and \
        d.x == params["col_idx"]*params["diam"] + params["diam"]/2 and \
        d.y == params["SPACE"]["h"] - params["rows"]*params["diam"]\
        - params["diam"]/2 and \
        d.lowest_point == params["SPACE"]["h"] - params["diam"] *\
        params["disks_of_col"] - params["diam"]/2
