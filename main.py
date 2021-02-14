# -*- coding: utf-8 -*-
"""Main app page"""

import re
from loglan_db import app_lod
from loglan_db.model import Word, Type

if __name__ == "__main__":

    with app_lod().app_context():
        # type_id = [t.id for t in Type.by(type_filter=["Cpd"]).all()]  # (C)V(V) # "Cpd" (C)V(V)[(C)V(V)]

        afx = Word.query.all()
        ids = []
        for a in afx:
            if re.search("(cdz|cvl|ndj|ndz|dcm|dct|dts|pdz|gts|gzb|svl|jdj|jtc|jts|jvr|tvl|kdz|vts|mzb)", a.name.lower()):
                # print(a.id_old, a.name, a.origin, a.origin_x)
                print(a)
                ids.append(str(a.id_old))

        print(len(ids))
        print(", ".join(ids))
        print("|".join(ids))
    # Parents for Afx = [Prim, Little words]
