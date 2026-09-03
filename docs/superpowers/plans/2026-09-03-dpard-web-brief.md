# D-PARD Web Brief Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build an English, single-page D-PARD technical brief in a standalone Git repository.

**Architecture:** A dependency-free static site uses one semantic HTML document and one stylesheet. Existing paper figures are copied into a local assets directory, and a Python standard-library contract test verifies the page structure, claims, links, and assets.

**Tech Stack:** HTML5, CSS3, MathJax CDN, Python 3 standard library, Git.

**Spec:** `docs/design.md`

## Global Constraints

- English only.
- Follow the current D-PARD paper's argument rather than reproducing the D-Cut page section-for-section.
- Keep the page concise and omit the confidence extension and internal framework details.
- Use no frontend framework, package manager, build step, or custom runtime JavaScript; MathJax is the only page script.
- Use only verified benchmark values from the paper table.
- Keep Rényi-half distinct from exact acceptance.

---

### Task 1: Page content and asset contract

**Files:**
- Create: `tests/test_site.py`
- Create: `index.html`
- Create: `assets/gradient-geometry.png`
- Create: `assets/position-credit.png`
- Create: `assets/acceptance-bound.png`

**Interfaces:**
- Consumes: the section order and content constraints in `docs/design.md`.
- Produces: an `index.html` document with stable section IDs and three local image paths.

- [x] **Step 1: Write the failing contract test**

  Use `html.parser.HTMLParser` to assert the title, language, required section
  IDs, exact headline gains, six benchmark names, three image paths, and the
  absence of banned internal terms.

- [x] **Step 2: Run the test to verify RED**

  Run: `python3 -m unittest tests/test_site.py -v`

  Expected: FAIL because `index.html` does not exist.

- [x] **Step 3: Copy the three paper figures**

  Copy the current English PNG files into the stable asset names declared by
  the test.

- [x] **Step 4: Implement the semantic HTML**

  Create a concise document with `overview`, `problem`, `bound`, `method`,
  `evidence`, and `implementation` sections, a sticky table of contents, the
  verified results table, collapsed proof, and collapsed core loss code.

- [x] **Step 5: Run the test to verify GREEN**

  Run: `python3 -m unittest tests/test_site.py -v`

  Expected: all tests pass.

### Task 2: Responsive presentation

**Files:**
- Modify: `tests/test_site.py`
- Create: `styles.css`
- Modify: `index.html`

**Interfaces:**
- Consumes: semantic classes and IDs from Task 1.
- Produces: a desktop article/contents layout and a one-column mobile layout.

- [x] **Step 1: Add a failing presentation contract**

  Assert that the stylesheet exists and contains the expected grid, sticky
  contents rail, restrained color variables, table overflow behavior, and a
  mobile breakpoint.

- [x] **Step 2: Run the test to verify RED**

  Run: `python3 -m unittest tests/test_site.py -v`

  Expected: FAIL because `styles.css` does not exist.

- [x] **Step 3: Implement the minimal stylesheet**

  Add typography, spacing, callouts, figure cards, minimal-rule tables,
  responsive behavior, focus states, and print styles without animation.

- [x] **Step 4: Run the test to verify GREEN**

  Run: `python3 -m unittest tests/test_site.py -v`

  Expected: all tests pass.

### Task 3: Documentation and visual verification

**Files:**
- Modify: `tests/test_site.py`
- Create: `README.md`

**Interfaces:**
- Consumes: completed static site.
- Produces: reproducible local preview instructions and verified desktop/mobile rendering.

- [x] **Step 1: Add a failing documentation contract**

  Assert that `README.md` names the project and contains the exact local server
  command `python3 -m http.server 8000`.

- [x] **Step 2: Run the test to verify RED**

  Run: `python3 -m unittest tests/test_site.py -v`

  Expected: FAIL because `README.md` does not exist.

- [x] **Step 3: Add concise usage documentation**

  Document the site purpose, local preview command, file layout, and source of
  the copied figures.

- [x] **Step 4: Run automated verification**

  Run: `python3 -m unittest discover -s tests -v`

  Expected: all tests pass.

- [x] **Step 5: Run visual verification**

  Serve the repo locally, inspect a desktop viewport and a mobile viewport,
  check browser console output, and revise any overflow or hierarchy defects.

- [x] **Step 6: Commit the completed repository**

  Run: `git add . && git commit -m "feat: add D-PARD technical brief"`
