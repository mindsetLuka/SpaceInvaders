def cross(obj1, obj2):
    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (dx, dy)) is not None
