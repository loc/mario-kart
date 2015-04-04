
def crop(m, s):
    x, y, w, h = s
    return m[y:y+h, x:x+w, ...]

def cropRect(m, s):
    (x, y), (x2, y2) = s
    return crop(m, (x, y, x2-x, y2-y))

def pointSizeToRect(s):
    (x, y), (w, h) = s
    return ((x, y), (x + w, y + h))
