def iter_rings(data, pathcodes):
    ring = []
    # TODO: Do this smartly by finding when pathcodes changes value and do
    # smart indexing on data, instead of iterating over each coordinate
    for point, code in zip(data, pathcodes):
        if code == 'M':
            # Emit the path and start a new one
            if len(ring):
                yield ring
            ring = [point]
        elif code == 'L':
            ring.append(point)
        else:
            raise ValueError('Unrecognized code: {}'.format(code))

    if len(ring):
        yield ring
