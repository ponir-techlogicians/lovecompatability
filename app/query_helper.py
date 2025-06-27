# utils.py
from geopy.distance import geodesic
from django.db.models import Q

RADIUS_MAP = {
    '1':   1,
    '2':  50,
    '3': 200,
    '4': float('inf'),
}

def filter_and_count(qs, query, latitude, longitude, radius_input):
    # 1) filter by name (substring, case-insensitive)
    if query:
        qs = qs.filter(
            Q(name1__icontains=query) |
            Q(name2__icontains=query)
        )

    # 2) apply radius filter
    if latitude and longitude and radius_input:
        try:
            user_loc = (float(latitude), float(longitude))
            km_limit = RADIUS_MAP.get(radius_input, 1)
        except ValueError:
            pass
        else:
            nearby = []
            for rec in qs:
                if rec.latitude is None or rec.longitude is None:
                    continue
                if geodesic(user_loc, (rec.latitude, rec.longitude)).km <= km_limit:
                    nearby.append(rec)
            qs = nearby

    # 3) make a plain Python list
    results = qs if isinstance(qs, list) else list(qs)

    # 4) count *exact* mentions (as before)
    mention_count = 0
    if query:
        ql = query.lower()
        for rec in results:
            if rec.name1.lower() == ql:
                mention_count += 1
            if rec.name2.lower() == ql:
                mention_count += 1

    return results, mention_count
