# clarify artwork — provenance

## Direction and production

Original, AI-assisted art direction and SVG/Python authoring by Mira for `luchasarie/claude-clarify`. The project brief and the existing README supplied the product behavior and required copy.

Visual summary: an open, imperfect loop resolves into a straight editable line and an insertion caret; ink green, warm white, and celadon communicate clarity without an automatic-send metaphor.

**Image-generation model: none.** No image-model output, image-model text, photography, stock imagery, people, third-party logos, or borrowed brand marks are used. Geometry is authored as editable SVG paths. All lettering is deterministic SVG text, not synthesized lettering. The flow is an explicitly labeled illustration, not a product screenshot.

Original artwork and authoring code are contributed under the repository's existing MIT license. No font binaries or external assets are bundled. Font software retains its own license.

## Release files

| File | How it was made | One-line brief / summary |
| --- | --- | --- |
| `.claude-plugin/icon.png` | Original text-free SVG paths from `assets/source/v2/icon.svg`; librsvg/Cairo rasterization at 2×, Pillow LANCZOS reduction and lossless PNG encoding. | A tangled ivory line resolves into a celadon line and insertion caret on an opaque ink-green square; recognizable at 32 px. |
| `assets/banner.png` | Layout, original vector illustration, and exact Fira Code/Lato typography in `assets/source/v2/banner.svg`; same deterministic raster pipeline. | Introduce “clarify” with the exact tagline “Rough request in. Clear prompt back in your prompt box, unsent.” and a schematic unsent prompt field. |
| `assets/before-after.png` | Two deliberately schematic input states, exact prompt text, labels and cursor in `assets/source/v2/before-after.svg`; same deterministic raster pipeline. | Show the supplied Safari-login request becoming the supplied clear draft in the same prompt box, unsent and waiting for Enter. |
| `assets/CREDITS.md` | Authored Markdown, checked against the actual source files, rendering tools, font metadata, and exports. | Record per-file provenance, font licenses, and reproduction notes. |

All three release PNGs are fully opaque RGB images. The banner and flow intentionally retain their warm-white background on either GitHub theme; the icon has an opaque green square, not transparent corners or a white matte.

## Editable sources

| File | Method / one-line summary |
| --- | --- |
| `assets/source/render-artwork.py` | AI-assisted Python authoring of original SVG geometry, deterministic typesetting, rendering, exact-copy assertions, type measurements, contrast checks, and contextual QA sheets. Current code produces the revised v2 design. |
| `assets/source/v2/icon.svg` | Final editable vector master: simplified two-opening loop, straight segment, insertion caret, opaque square and quiet inset keyline; no text elements. |
| `assets/source/v2/banner.svg` | Final editable hero master: exact wordmark/tagline, original clarification motif, invocation examples, and user-control message. |
| `assets/source/v2/before-after.svg` | Final editable flow master: exact supplied drafts, two states of one prompt field, unsent badge, insertion cursor and Enter hint. |

SVG masters retain editable text. Re-rendering requires the named fonts; the release PNGs have no font dependency.

## Proofs and QA evidence

Running `assets/source/render-artwork.py` writes proof renders, light/dark theme sheets and computed checks (dimensions, exact copy, contrast) to `assets/artwork-qa/`, which is git-ignored. The release PNGs were reviewed from those proofs before export.

## Tools and fonts

Production tools actually used:

- System Python 3, PyGObject/librsvg 2.61.3, Cairo 1.18.4, and Pillow 12.1.1.
- SVG rasterization at twice the delivery dimensions, followed by LANCZOS downsampling and lossless RGB PNG encoding.
- Hermes image/vision inspection for full-size exports and the light/dark contextual sheet. No generative image tool was called.
- Python XML parsing for exact visible-copy checks; Pango for line-width measurements; SHA-256 and Pillow for file verification.

Typography:

- **Fira Code**, regular and medium: wordmark, commands, prompt text, and utility labels. The inspected Medium font identifies itself as version 6.002, copyright 2014–2021 The Fira Code Project Authors, licensed under SIL Open Font License 1.1. Source: https://github.com/tonsky/FiraCode . License reference: https://openfontlicense.org/ .
- **Lato**, regular and bold: explanatory copy and headings. Copyright Łukasz Dziedzic; SIL Open Font License 1.1, verified in the system package's copyright file. Source: https://www.latofonts.com/ .
- **DejaVu Sans Mono**, contextual-QA labels only. Source/license: https://dejavu-fonts.github.io/License.html .

The SVG sources reference font family names; they do not embed or redistribute font software.

## Reproduction

From the repository root, on a system with the dependencies/fonts above:

```sh
/usr/bin/python3 -B assets/source/render-artwork.py --variant fresh-review
```

Use a **new** variant name. The script refuses to replace existing proofs and refuses to alter an existing source with different content. It writes only beneath this repository. It creates sources, PNG proofs, a contextual sheet, and checks; it deliberately does not overwrite the reviewed release paths. Review any new variant before choosing it for a future release.

## Text alternatives

- Icon: “clarify: a tangled line becomes a clear line and insertion caret.”
- Banner: “clarify: rough request in, clear prompt back in your prompt box, unsent.”
- Flow: “A rough request ending in --clarify becomes a clearer draft in the same prompt box. The rewrite stays unsent for review and editing; press Enter to send.”

The exact sample drafts also appear as real text in the existing README, so the illustration is not the sole source of that information.
