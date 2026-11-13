# Raspberry Pi 4 Model B board reconstruction

A KiCad 10 reconstruction of the Raspberry Pi 4 Model B board (part placement, part identification, nets traced from
real boards), published as interactive boardviews for repair work. Each board revision is reconstructed separately.

> [!WARNING]
> **Unofficial, incomplete and possibly wrong.**
> * **Not official.** Not made, endorsed or checked by Raspberry Pi Ltd, and not based on official schematics or layout
>   files. "Raspberry Pi" is a trademark of Raspberry Pi Ltd; this project is not affiliated with it.
> * **Made by a hobbyist.** Reverse engineered by an untrained hobbyist from photos and multimeter probing, not by an
>   electronics professional.
> * **Incomplete and possibly wrong.** Many parts are unidentified and most nets are untraced. Positions, values, part
>   numbers and connections may be wrong, and your board may differ.
> * **Use at your own risk.** Board-level repair can destroy hardware and can be dangerous. Check everything against
>   your own board, your own measurements and the manufacturers' datasheets before you solder or apply power. Provided
>   "as is" with no warranty of any kind; the authors and contributors accept no liability for any damage or injury.

* **View it:** <https://dpetzel.github.io/pi4-boardview/> lists the revisions, rebuilt from `main` on every push

| Revision | Viewer | Downloads (always the latest build) | Status |
|---|---|---|---|
| 1.4 | [pi4-boardview/1.4/](https://dpetzel.github.io/pi4-boardview/1.4/) | [HTML](https://dpetzel.github.io/pi4-boardview/1.4/pi4_rev_1.4-boardview.html) · [.brd](https://dpetzel.github.io/pi4-boardview/1.4/pi4_rev_1.4.brd) | In progress |
| 1.5 | [pi4-boardview/1.5/](https://dpetzel.github.io/pi4-boardview/1.5/) | [HTML](https://dpetzel.github.io/pi4-boardview/1.5/pi4_rev_1.5-boardview.html) · [.brd](https://dpetzel.github.io/pi4-boardview/1.5/pi4_rev_1.5.brd) | Photos aligned, no parts yet |

The HTML viewer is self-contained and works offline; the `.brd` is for
[OpenBoardView](https://github.com/OpenBoardView/OpenBoardView). The revision is printed on the board's top silkscreen.

## Repository

| Path | What |
|---|---|
| `1.4/`, `1.5/` | One KiCad project per board revision (`pi4_rev_<rev>.kicad_pcb`, `.kicad_pro`, `.kicad_sch`). Top and bottom photos are embedded in each board as reference images (Eco1.User = top, Eco2.User = bottom) |
| `1.4/*.kicad_sch`, `1.4/pi4_rev_1.4.kicad_sym` | Rev 1.4 schematic (root sheet plus `board_only` and `top_ics` sub-sheets) and its symbols |
| `lib/pi4_common.pretty/`, `lib/pi4_common.kicad_sym` | Footprints and symbols shared by all revisions (`${KIPRJMOD}/../lib` in each revision's lib tables) |
| `tools/boardview.py`, `tools/template.html` | Exporter for one board (HTML viewer + `.brd`) and the viewer it fills in |
| `tools/build_site.py`, `tools/index.html` | Builds every revision plus the landing page that lists them |
| `.github/workflows/boardview.yml` | CI: builds the boardviews and deploys them to Pages |

The boardview files are build output and not committed.

### Adding a revision

Make a folder named after the revision (e.g. `1.2/`) holding one KiCad project, `pi4_rev_1.2.kicad_pcb` with the
board photos embedded as reference images. `build_site.py` picks up every top-level folder named like a version number,
so the new revision appears on the site and in every viewer's revision switcher on the next push. Add it to the table
above.

## Contributing

Edit a board in KiCad 10 and open a pull request. Part details go in footprint fields: `Function`, `Part`, `Notes`,
`Replacement`, and `Source` (`Source2`, `Source3`, … for more links). Fields holding a URL show as links in the
viewer. References ending in `**` or `?` (`REF**`, `R?`) are shown as unidentified parts.

Every pull request builds the boardviews. Download the `boardview` artifact from the PR's workflow run to check
your change before it's merged.

### Building locally

The exporter needs KiCad's `pcbnew` Python module. With Docker:

```sh
docker run --rm -v "$PWD":/w -w /w kicad/kicad:10.0 python3 tools/build_site.py
```

or with the Python bundled with KiCad (on Windows, `"C:\Program Files\KiCad\10.0\bin\python.exe"`):

```sh
python3 tools/build_site.py                       # all revisions -> _site/ (open _site/index.html)
python3 tools/boardview.py 1.4/pi4_rev_1.4.kicad_pcb   # one board -> 1.4/boardview/
```

Options for both: `-o DIR`, `--no-photo`, `--kicad-nets-only` (skip nets derived from copper; see the notes at the top
of `tools/boardview.py`). The revision switcher only shows when the site is served over http(s), e.g.
`python3 -m http.server -d _site`. KiCad exports the last *saved* board, so save before building.

## License

[CC-BY-SA-4.0](LICENSE): share and adapt with attribution, and publish adaptations under the same license.
The license's disclaimer of warranties and limitation of liability apply in full.
