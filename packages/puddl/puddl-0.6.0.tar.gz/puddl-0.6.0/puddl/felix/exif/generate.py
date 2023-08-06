#!/usr/bin/env python

import json

from puddl.db.alchemy import App

app = App('exif')

data = []
rows = app.engine.execute('SELECT * FROM markers')

for row in rows:
    d = dict(zip(rows.keys(), row))
    data.append(d)

jsdata = json.dumps(data)
print(f"window.exif_data = {jsdata}")
