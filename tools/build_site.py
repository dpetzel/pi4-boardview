"""Build the boardview site for every board revision: one viewer per revision plus a landing page that lists them.

Usage: build_site.py [-o OUTDIR] [--no-photo] [--kicad-nets-only]       (run from anywhere; default OUTDIR: _site)

A revision is a top-level directory named like a version number (1.4, 1.5, ...) holding one .kicad_pcb. Writes
  OUTDIR/index.html                          landing page (tools/index.html filled in)
  OUTDIR/<rev>/index.html                    the viewer, so <site>/<rev>/ opens it
  OUTDIR/<rev>/<board>-boardview.html        the same viewer under its own name, for download (works offline)
  OUTDIR/<rev>/<board>.brd                   OpenBoardView
Each viewer gets a revision switcher, shown only when it is served over http(s) where the sibling revisions exist."""
import argparse, glob, html, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import boardview  # noqa: E402  (needs pcbnew)

BOARD = 'Raspberry Pi 4 Model B'


def revisions():
    revs = []
    for d in sorted(os.listdir(ROOT), key=lambda n: [int(x) for x in n.split('.')] if re.fullmatch(r'\d+(\.\d+)*', n) else []):
        if not re.fullmatch(r'\d+(\.\d+)*', d):
            continue
        pcbs = glob.glob(os.path.join(ROOT, d, '*.kicad_pcb'))
        if len(pcbs) != 1:
            sys.exit('%s: expected one .kicad_pcb, found %d' % (d, len(pcbs)))
        revs.append((d, pcbs[0]))
    if not revs:
        sys.exit('no board revisions found under ' + ROOT)
    return revs


def card(rev, d, files):
    parts = d['parts']
    unident = sum(p['ref'].endswith(('**', '?')) for p in parts)
    nets = len({q[7] for p in parts for q in p['pads'] if q[7]})
    stats = ('%d parts (%d unidentified), %d nets' % (len(parts), unident, nets)) if parts else 'Photos only: no parts placed yet'
    e = html.escape
    return ('<li><a class="open" href="%s/"><b>Rev %s</b><span>%s</span></a>'
            '<span class="dl">Download: <a href="%s/%s" download>HTML</a> · <a href="%s/%s" download>.brd</a></span></li>'
            % (e(rev), e(rev), e(stats), e(rev), e(files['html'][0]), e(rev), e(files['brd'][0])))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('-o', '--out', default=os.path.join(ROOT, '_site'), help='output directory (default: _site)')
    ap.add_argument('--no-photo', action='store_true', help='leave out the embedded reference photos')
    ap.add_argument('--kicad-nets-only', action='store_true', help="don't derive nets from copper geometry")
    a = ap.parse_args()
    revs = revisions()
    nav = [{'id': r, 'label': 'Rev ' + r, 'href': '../%s/' % r} for r, _ in revs]
    cards = []
    for rev, pcb in revs:
        d = boardview.load(pcb, derive=not a.kicad_nets_only)
        d.update(name='%s rev %s' % (BOARD, rev), rev=rev, revs=nav)
        out = os.path.join(a.out, rev)
        files = boardview.export(d, out, photo=not a.no_photo)
        shutil.copyfile(os.path.join(out, files['html'][0]), os.path.join(out, 'index.html'))
        cards.append(card(rev, d, files))
    page = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read().replace('<!--REVISIONS-->', '\n'.join(cards))
    boardview.write(os.path.join(a.out, 'index.html'), page)
    print('%s: %d revisions (%s)' % (os.path.join(a.out, 'index.html'), len(revs), ', '.join(r for r, _ in revs)))


if __name__ == '__main__':
    main()
