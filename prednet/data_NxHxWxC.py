import datetime as dt
from pathlib import Path

import hickle as hkl
import numpy as np
from PIL import Image


factor = 4
height, width = int(672 / factor), int(512 / factor)
channel = 1
inputs_d = Path('../inputs')
output_d = inputs_d/'hkl/'


def dump_hkl(start, end, datetime_format='%Y-%m-%d %H:%M'):
    start_dt = dt.datetime.strptime(start, datetime_format)
    end_dt = dt.datetime.strptime(end, datetime_format)
    assert start_dt.year == end_dt.year
    year = start_dt.year

    logf = open(f'../inputs/missing_{year}.list', 'a')
    data_d = inputs_d/'test/sat/' if year == 2018 else inputs_d/'train/sat/'

    im_list = []
    source_list = []
    current_dt = start_dt
    while current_dt <= end_dt:
        y, m, d, h = current_dt.year, current_dt.month, current_dt.day, current_dt.hour
        dname = f'{y:0>2}-{m:0>2}-{d:0>2}'
        fname = f'{dname}-{h:0>2}-00.fv.png'
        impath = (data_d/dname/fname)
        if impath.is_file():
            im = Image.open(impath).convert('L')
            im = im.resize((width, height))
            im = np.asarray(im)[:, :, np.newaxis]
        else:
            im = np.zeros((height, width, channel))
            print(f'File not found: {fname}', file=logf)
        im_list.append(im)
        source_list.append(f'{year}')
        current_dt = current_dt + dt.timedelta(hours=1)

    X = np.stack(im_list, axis=0)
    path = output_d/f'X_{year}_{height}x{width}x{channel}.hkl'
    hkl.dump(X, path.as_posix())
    print(f'Dumped at {path}')
    path = output_d/f'source_{year}_{height}x{width}x{channel}.hkl'
    hkl.dump(source_list, path.as_posix())
    print(f'Dumped at {path}')

    logf.close()

    return X, source_list


if __name__ == '__main__':
    X_2016, source_2016 = dump_hkl('2016-01-01 00:00', '2016-12-31 23:00')
    X_2017, source_2017 = dump_hkl('2017-01-01 00:00', '2017-12-31 23:00')
    dump_hkl('2018-01-01 00:00', '2018-12-31 23:00')

    p = output_d/f'X_2016+2017_{height}x{width}x{channel}.hkl'
    hkl.dump(np.concatenate([X_2016, X_2017], axis=0), p.as_posix())
    p = output_d/f'source_2016+2017_{height}x{width}x{channel}.hkl'
    hkl.dump(source_2016 + source_2017, p.as_posix())
