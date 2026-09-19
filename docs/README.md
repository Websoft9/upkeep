# UpKeep Documentation

This directory contains the UpKeep product documentation, built with
[Docusaurus](https://docusaurus.io/). The documentation is authored in **English
by default**. Additional locales can be added later through Docusaurus
internationalization.

## Layout

```
docs/
├── docs/                 # Documentation content (Markdown / MDX)
│   ├── intro.md
│   ├── getting-started/  # Installation and quickstart
│   ├── concepts/         # Architecture, data model, rules
│   ├── api/              # HTTP API reference
│   └── product/          # Business brief and MVP PRD
├── src/                  # Custom pages and components
├── static/               # Static assets (images, favicon)
├── docusaurus.config.js  # Site configuration
└── sidebars.js           # Sidebar configuration
```

## Requirements

- Node.js 20 or newer

## Local development

```bash
npm install
npm run start
```

The dev server listens on `http://localhost:3000/upkeep/`.

## Build

```bash
npm run build     # produce a static site in build/
npm run serve     # preview the production build locally
```

## Authoring

- Add pages under `docs/docs/`; the sidebar is generated from the folder
  structure.
- Control ordering with `sidebar_position` front matter and `_category_.json`
  files.
- Keep every example in English unless a translation is being added.

From the repository root you can also use:

```bash
make docs-install
make docs-run
make docs-build
```
