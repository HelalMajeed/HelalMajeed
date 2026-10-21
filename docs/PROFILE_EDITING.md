# Crescent profile

The public `HelalMajeed/HelalMajeed` repository supplies the README displayed on the `HelalMajeed` GitHub profile.

## Editing

- Edit `README.md` for the biography, projects, links, and toolkit.
- Edit `scripts/generate-assets.py` for banner typography, palette, and geometry. Run `python3 scripts/generate-assets.py` to regenerate all six assets.
- Commit the SVG outputs with any generator change; there is no runtime build or scheduled workflow.

## Design

The visual identity uses Crescent's name as an orbital motif: a custom crescent, fine orbital paths, quiet mint/lime accents, and editorial typography. The main SVGs contain a larger-type compact composition selected by an internal width media query. The standalone tall mobile SVGs are optional alternate artwork. The README uses GitHub's native text, links, headings, and tables below the banner.

Light and dark themes use native HTML `picture` sources. GitHub rewrites picture media attributes to match the selected GitHub theme, so width breakpoints must remain inside the SVG rather than on picture sources. Motion is CSS-only inside the SVG and respects `prefers-reduced-motion`. The resting frame is complete if animation is unavailable. Images include text alternatives. There is no JavaScript, remote font, profile tracking pixel, external badge service, or GitHub Actions dependency.

GitHub controls the surrounding profile layout, avatar, bio, pinned repositories, and contribution graph. A README cannot replace those with a custom website layout.

## Content basis

Prepared on 2026-10-21 from the connected account identity and the public Radiant, FREEZONE, Data Structures, and Projects4Fun repositories. OORR links point to its public product and documentation; private source repositories are not linked or published. No credentials, personal email address, unsupported employment history, follower metrics, skill percentages, or claims of model ownership are included.

Reference: https://github.com/MAZHARMIK was reviewed for structure. All profile wording and artwork here are original.

Suggested pins, if desired: `radiant`, `freezone-website`, `Datastructure_Implementations`, and `Projects4Fun`.
