#!/usr/bin/env python
import base64
import logging
from pathlib import Path

import exifread
import pandas as pd

from puddl.db.alchemy import App

log = logging.getLogger()

img_dir = Path('/home/felix/Seafile/s7-camera/My Photos/Camera/')
imgs = list(img_dir.glob('*.jpg'))
# imgs = list(img_dir.glob('20200831_160821.jpg'))
log.info(f'processing {len(imgs)} images')


def img2dict(path: Path):
    result = {
        '_path': str(path),
        '_name': path.name
    }
    with path.open('rb') as f:
        result.update(exifread.process_file(f))
    if 'JPEGThumbnail' in result:
        payload = base64.b64encode(result['JPEGThumbnail']).decode('utf-8')
        img = 'data:image/jpeg;base64,' + payload
    else:
        img = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQ' \
              'AAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
    result['thumb'] = img
    return result


def _exifread2pg_dict(d):
    result = {}
    for k, v in d.items():
        if isinstance(v, exifread.classes.IfdTag):
            result[k] = v.printable
        else:
            result[k] = v
    return result


def iter_imgs(imgs):
    for img in imgs:
        d = img2dict(img)
        yield _exifread2pg_dict(d)


app = App('exif')
log.info(app.engine)

df = pd.DataFrame(iter_imgs(imgs))
app.df_dump(df, 's7')
