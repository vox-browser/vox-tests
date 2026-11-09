#!/usr/bin/env python3
"""Capture native pixels for saved-canvas chains ending in a large blur."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
from native_fixture_hashes import Reference, background, segment


def capture(library, fixtures, output, verify):
    cases = json.loads(fixtures.read_text())
    pins = [library, fixtures, Path(__file__), Path(__file__).with_name('native_fixture_hashes.py')]
    hashes = {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}
    ref = Reference(library)
    field = 'expected_linux' if platform.system() == 'Linux' else 'expected_macos'
    for i, c in enumerate(cases):
        s = c['shape_scale']
        path = (segment(0, 10*s, 8*s) + segment(2, 38*s, 12*s, 40*s, 30*s)
                + segment(1, 12*s, 34*s) + segment(5))
        if c.get('rectangle'):
            path = (segment(0, -1024, -1024) + segment(1, 1024, -1024)
                    + segment(1, 1024, 1024) + segment(1, -1024, 1024) + segment(5))
        triangle = segment(0, 2, 3) + segment(1, 45.5, 10.25) + segment(1, 20.5, 38) + segment(5)
        style = dict(width=7, height=6, premultiplied=False, display_p3=True,
                     transform=[1, 0, 0, 1, 0, 0]) if c['pattern'] else None
        digest = ref.path(background(48, 40, 'image'), 48, 40, path, f'terminal-blur-{i}',
                          c['expected_macos'], transform=c['transform'], color=0xc0e04010, alpha=.7,
                          alpha_type=c['alpha_type'], mode=c['mode'], style=style,
                          stroke=(3, 1, 0, 10, [3, 2], .7) if c['stroke'] else None,
                          clips=[(triangle, False)] if c['clipped'] else [], filters=c['filters'])
        if verify:
            assert digest == c[field], (i, digest, c[field])
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in hashes.items())
    output.write_text(json.dumps(dict(platform=platform.platform(), input_sha256=hashes,
                                     records=ref.records), indent=2)+'\n')
    print(f'{len(cases)} native terminal-blur fixtures'+(' verified' if verify else ' captured'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('library', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    capture(args.library, args.fixtures, args.output, args.verify)
