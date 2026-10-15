# Website maintenance

The live academic website is the static site in this `docs` directory. The older Jekyll source remains in the repository root for reference and recovery. GitHub Pages should publish `master` → `/docs`.

- Edit biography, research, appointments and teaching in `docs/index.html`.
- Edit journal articles in `docs/assets/publications.json`. Use the correct publication year and category (`ai`, `fire`, or `materials`). Set `selected` to `true` for homepage highlights. Only add DOI URLs you have verified; otherwise the site provides a title search link.
- After editing content, run `python scripts/build_academic_site.py` from the repository root. This updates publication HTML, BibTeX, the public CV, sitemap and redirects. No third-party Python packages are required.
- Preview with `python -m http.server 8765 --directory docs`, then open `http://localhost:8765`.
- Commit and push to `master` to publish. No Node, Ruby, database or paid hosting is needed.

The public CV is an adapted version of the private August 2026 CV. The original Word document, telephone number and referee emails are not published. Manuscript statuses are explicitly tied to that CV date. Update the status text when new information is available.

The homepage illustration is a conceptual structural mesh drawn with SVG. It is not research data, a numerical result or an experimental image. The site uses system fonts and has no analytics, tracking cookies or external JavaScript dependencies. Publication content works without JavaScript; JavaScript enhances filters, mobile navigation and the schematic mesh.
