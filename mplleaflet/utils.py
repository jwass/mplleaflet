import json
from json.encoder import JSONEncoder


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
        elif code == 'L' or code == 'Z' or code == 'S':
            ring.append(point)
        else:
            raise ValueError('Unrecognized code: {}'.format(code))

    if len(ring):
        yield ring


class FloatEncoder(JSONEncoder):
    _formatter = ".3f"

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.
        For example::
            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)
        """
        c_make_encoder_original = json.encoder.c_make_encoder
        json.encoder.c_make_encoder = None

        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = json.encoder.encode_basestring_ascii
        else:
            _encoder = json.encoder.encode_basestring

        def floatstr(o, allow_nan=self.allow_nan,
                     _repr=lambda x: format(x, self._formatter),
                     _inf=float("inf"), _neginf=-float("inf")):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.
            if o != o:
                text = 'NaN'
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError(
                    "Out of range float values are not JSON compliant: " +
                    repr(o))

            return text

        if (_one_shot and json.encoder.c_make_encoder is not None
                and self.indent is None):
            _iterencode = json.encoder.c_make_encoder(
                markers, self.default, _encoder, self.indent,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, self.allow_nan)
        else:
            _iterencode = json.encoder._make_iterencode(
                markers, self.default, _encoder, self.indent, floatstr,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, _one_shot)
        json.encoder.c_make_encoder = c_make_encoder_original
        return _iterencode(o, 0)
