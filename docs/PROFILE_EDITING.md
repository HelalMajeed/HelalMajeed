# Crescent profile

The public `HelalMajeed/HelalMajeed` repository supplies the README displayed on the `HelalMajeed` GitHub profile.

## Editing

- Edit `docs/PROFILE_TEXT.md` for the accessible text version of the biography, projects, links, and toolkit.
- Edit `scripts/generate-sections.py` for the section artwork, project cards, icons, links, and README structure. Run `python3 scripts/generate-sections.py` to regenerate the 20 section SVGs, `README.md`, and `docs/ARTWORK_PREVIEW.md`.
- Edit `scripts/generate-assets.py` for banner typography, palette, and geometry. Run `python3 scripts/generate-assets.py` to regenerate all six assets.
- Commit the SVG outputs with any generator change; there is no runtime build or scheduled workflow.

## Design

The visual identity uses Crescent's name as an orbital motif: a custom crescent, fine orbital paths, quiet mint/lime accents, and editorial typography. Matching panels cover the introduction, OORR AI, four selected projects, toolkit, research interests, and contact. Original animated icons include a blinking tutor, voice bars, a rotating sun, commerce cube, data nodes, and terminal.

The main SVGs contain a larger-type compact composition selected by an internal width media query. The standalone tall mobile SVGs are optional alternate artwork. The README retains native text and links inside an expandable text version. `docs/ARTWORK_PREVIEW.md` displays each section at 360 pixels in both themes for compact rendering checks.

Light and dark themes use native HTML `picture` sources. GitHub rewrites picture media attributes to match the selected GitHub theme, so width breakpoints must remain inside the SVG rather than on picture sources. Motion is CSS-only inside the SVG and respects `prefers-reduced-motion`. The resting frame is complete if animation is unavailable. Images include text alternatives. There is no JavaScript, remote font, profile tracking pixel, external badge service, or GitHub Actions dependency.

GitHub controls the surrounding profile layout, avatar, bio, pinned repositories, and contribution graph. A README cannot replace those with a custom website layout.

## Content basis

Prepared on 2026-10-21 from the connected account identity and the public Radiant, FREEZONE, Data Structures, and Projects4Fun repositories. OORR links point to its public product and documentation; private source repositories are not linked or published. No credentials, personal email address, unsupported employment history, follower metrics, skill percentages, or claims of model ownership are included.

Reference: https://github.com/MAZHARMIK was reviewed for structure. All profile wording and artwork here are original.

Suggested pins, if desired: `radiant`, `freezone-website`, `Datastructure_Implementations`, and `Projects4Fun`.
