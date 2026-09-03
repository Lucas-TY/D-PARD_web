from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.images = []
        self.icons = []
        self.links = []
        self.lang = None
        self.text = []
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "html":
            self.lang = attributes.get("lang")
        if tag == "img":
            self.images.append(attributes.get("src"))
        if tag == "link" and attributes.get("rel") == "icon":
            self.icons.append(attributes.get("href"))
        if tag == "a":
            self.links.append(attributes.get("href"))
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        self.text.append(data)
        if self._in_title:
            self.title += data


class SiteContentContract(unittest.TestCase):
    def test_page_matches_the_dpard_brief_contract(self):
        page = ROOT / "index.html"
        self.assertTrue(page.exists(), "index.html must exist")

        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        visible_text = " ".join(parser.text)

        self.assertEqual(parser.lang, "en")
        self.assertIn("D-PARD", parser.title)
        self.assertEqual(
            {"overview", "problem", "bound", "method", "evidence", "implementation"},
            {section for section in parser.ids if section in {
                "overview", "problem", "bound", "method", "evidence", "implementation"
            }},
        )
        self.assertIn("6.29%", visible_text)
        self.assertIn("4.02%", visible_text)
        for benchmark in ("GSM8K", "MATH-500", "HumanEval", "MBPP", "MT-Bench", "Alpaca"):
            self.assertIn(benchmark, visible_text)

        self.assertEqual(
            parser.images,
            [
                "assets/gradient-geometry.png",
                "assets/position-credit.png",
                "assets/acceptance-bound.png",
            ],
        )
        for image in parser.images:
            self.assertTrue((ROOT / image).is_file(), f"missing {image}")

        self.assertEqual(parser.icons, ["assets/favicon.svg"])
        self.assertTrue((ROOT / "assets/favicon.svg").is_file())
        for url in (
            "https://github.com/Lucas-TY/D-PARD",
            "https://github.com/vllm-project/speculators/pull/1076",
            "https://github.com/sgl-project/SpecForge/pull/824",
        ):
            self.assertIn(url, parser.links)
        self.assertIn("position-weight mass", visible_text)
        self.assertIn("earlier valid-position experiment", visible_text)

        for banned in (
            "D-PACKL",
            "credit_calibration",
            "source binding",
            "commit",
            "tells us",
            "remain fragile",
            "probability-like",
        ):
            self.assertNotIn(banned, visible_text)

    def test_stylesheet_supports_docs_layout_and_mobile_reading(self):
        stylesheet = ROOT / "styles.css"
        self.assertTrue(stylesheet.exists(), "styles.css must exist")
        css = stylesheet.read_text(encoding="utf-8")

        for contract in (
            "--blue:",
            "--peach:",
            "--green:",
            "grid-template-columns:",
            "position: sticky",
            "overflow-x: auto",
            "@media (max-width: 860px)",
            ":focus-visible",
            "@media print",
            ".summary-results table",
            ".benchmark-details",
        ):
            self.assertIn(contract, css)

    def test_page_has_a_compact_method_story(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="reading-progress"', html)
        self.assertIn('class="concept-strip"', html)
        self.assertIn('<h1><span class="method-name">D-PARD:</span>', html)
        self.assertIn("Deployment metric", html)
        self.assertIn("Position credit", html)
        self.assertIn("Local geometry", html)
        self.assertIn("divergence-form extension of D-PACE", html)
        self.assertIn("certified lower bound on exact acceptance", html)
        self.assertIn("without introducing a second proposal objective", html)
        self.assertIn("D-PACE's position-credit decomposition", html)
        self.assertIn("q_y(q-e_y)", html)
        self.assertIn("DSpark: fixed CE+TV", html)
        self.assertIn("LK: adaptive KL+TV", html)
        self.assertIn("LK: log acceptance", html)
        self.assertEqual(html.count('class="remedy-family'), 2)
        self.assertIn("Family 1 · Fused losses", html)
        self.assertIn("Family 2 · Rescaled TV", html)
        self.assertNotIn('class="equation small"', html)
        self.assertNotIn("g_{\\mathrm{mix},t}", html)
        self.assertIn("trajectory credit and local difficulty", html)
        self.assertIn("loss-curriculum warm-up", html)
        self.assertIn("confidence head remains unchanged", html)
        self.assertNotIn("<td>Static</td><td>D-PARD</td>", html)
        self.assertIn('class="table-wrap summary-results"', html)
        self.assertIn('class="benchmark-details"', html)
        self.assertIn("Full six-benchmark results", html)
        self.assertEqual(html.count('class="equation'), 7)

    def test_motion_is_subtle_and_accessible(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        for contract in (
            "@keyframes hero-rise",
            "animation-timeline: scroll(root)",
            "animation-timeline: view()",
            "@media (prefers-reduced-motion: reduce)",
            ".reading-progress",
        ):
            self.assertIn(contract, css)
        self.assertNotIn(".hero::before", css)
        self.assertIn("font-size: clamp(2.75rem, 5.6vw, 4.65rem)", css)

    def test_readme_documents_the_zero_build_preview(self):
        readme = ROOT / "README.md"
        self.assertTrue(readme.exists(), "README.md must exist")
        text = readme.read_text(encoding="utf-8")
        self.assertIn("# D-PARD", text)
        self.assertIn("python3 -m http.server 8000", text)
        self.assertNotIn("Repository layout", text)
        self.assertNotIn("Run the checks", text)
        self.assertLessEqual(len(text.splitlines()), 10)

    def test_readthedocs_config_publishes_the_static_site(self):
        config = ROOT / ".readthedocs.yaml"
        self.assertTrue(config.exists(), ".readthedocs.yaml must exist")
        text = config.read_text(encoding="utf-8")
        for contract in (
            "version: 2",
            "os: ubuntu-24.04",
            'python: "3.12"',
            "build:",
            "html:",
            "mkdir -p $READTHEDOCS_OUTPUT/html/",
            "cp index.html styles.css $READTHEDOCS_OUTPUT/html/",
            "cp -R assets $READTHEDOCS_OUTPUT/html/assets",
        ):
            self.assertIn(contract, text)
        self.assertNotIn("sphinx:", text)
        self.assertNotIn("mkdocs:", text)


if __name__ == "__main__":
    unittest.main()
