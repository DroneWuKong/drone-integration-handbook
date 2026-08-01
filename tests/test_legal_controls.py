from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PUBLICATION_CONTROLS = {
    "field/ew-countermeasures.md": {
        "hold_markers": ("Publication Hold",),
        "review_record": "docs/reviews/rf-interference-and-spectrum-survey-2026-07-31.md",
        "forbidden": (
            "whether you're hunting the jammer",
            "map the EW bubble",
            "hunter-killer operations",
        ),
    },
    "field/intercept-ops.md": {
        "hold_markers": ("Publication Hold",),
        "review_record": "docs/reviews/civil-drone-encounter-safety-2026-07-31.md",
        "forbidden": (
            "full throttle through impact",
            "aim for the propellers",
            "recommended for beginners: stern chase",
            "use the entire drone as the weapon",
        ),
    },
    "field/elint-operators.md": {
        "hold_markers": ("Publication Hold",),
        "review_record": "docs/reviews/rf-interference-and-spectrum-survey-2026-07-31.md",
        "forbidden": (
            "vector an interceptor",
            "build a target package",
            "jammer triangulation",
            "allocate jamming resources",
        ),
    },
    "components/military-firmware-forks.md": {
        "hold_markers": ("Publication Hold",),
        "review_record": "docs/reviews/conflict-firmware-overview-2026-07-31.md",
        "forbidden": (
            "ciajeepdoors",
            "unique tx binding key required",
            "ew hunter-killer drones",
            "vtx frequency unlock",
        ),
    },
    "components/remote-id-custom-builds.md": {
        "hold_markers": ("Accuracy Hold", "Publication Hold"),
        "review_record": "docs/reviews/remote-id-custom-builds-2026-07-31.md",
        "forbidden": (
            "set drone_serial",
            "serial_passthrough",
            "bluemark db202",
            "multiple aircraft on one registration",
        ),
    },
    "components/ndaa-compliance.md": {
        "hold_markers": ("Accuracy Hold", "Publication Hold"),
        "review_record": "docs/reviews/federal-uas-procurement-2026-07-31.md",
        "forbidden": (
            "foci test clean",
            "non-covered origins (generally safe)",
            "chinese-born founders",
            "standard ear99 classification",
        ),
    },
    "components/orqa-hardware-guide.md": {
        "hold_markers": ("Review Hold", "Publication Hold"),
        "review_record": None,
        "forbidden": (
            "standard ear99 classification",
            "country: croatia (eu) — ndaa compliant",
        ),
    },
    "integration/wingman-apb.md": {
        "hold_markers": ("Review Hold", "Publication Hold"),
        "review_record": None,
        "forbidden": (
            "2.3 tops npu",
            "full autonomous control",
        ),
    },
}


class LegalContainmentTestCase(unittest.TestCase):
    def test_held_or_reviewed_pages_enforce_publication_state_and_regressions(self) -> None:
        """A page may stay held or enter review, but withdrawn text may not return."""

        for relative, controls in PUBLICATION_CONTROLS.items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                folded = text.casefold()

                for forbidden in controls["forbidden"]:
                    self.assertNotIn(forbidden.casefold(), folded)

                self.assertIn("jeremiah@midwestniceuas.com", text)
                is_held = any(marker in text for marker in controls["hold_markers"])

                if is_held:
                    continue

                review_relative = controls["review_record"]
                self.assertIsNotNone(
                    review_relative,
                    f"{relative} cannot leave hold without a mapped review record",
                )
                self.assertIn("**Verified:**", text)
                self.assertTrue(
                    "**Scope:**" in text or "**Primary scope:**" in text,
                    f"{relative} must state its public scope",
                )

                review_path = ROOT / str(review_relative)
                self.assertTrue(
                    review_path.is_file(),
                    f"reviewed replacement is missing {review_relative}",
                )
                review = review_path.read_text(encoding="utf-8")
                self.assertIn("Publication status", review)
                self.assertIn("Reviewer disposition", review)
                self.assertIn("Publisher release decision", review)

    def test_legal_pages_and_material_relationship_disclosure_exist(self) -> None:
        required_pages = [
            "legal/publisher-and-affiliations.md",
            "legal/editorial-and-corrections-policy.md",
            "legal/privacy.md",
            "legal/terms-and-disclaimer.md",
            "legal/ip-and-takedown.md",
        ]
        for relative in required_pages:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

        template = (ROOT / "templates/handbook.html").read_text(encoding="utf-8")
        self.assertIn("Jeremiah Wong", template)
        self.assertIn("Orqa Inc.", template)
        self.assertIn("Midwest Nice Advisory LLC", template)
        self.assertIn("jeremiah@midwestniceuas.com", template)

    def test_behavioral_analytics_are_not_present_in_handbook_client(self) -> None:
        script = (ROOT / "assets/handbook.js").read_text(encoding="utf-8")
        for marker in (
            "uas-forge.com/api/analytics/ingest",
            "__hbAnalytics",
            "session_id",
            "scroll_depth",
            "outbound_link",
        ):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, script)
        self.assertIn("Search stays in this browser tab", script)


if __name__ == "__main__":
    unittest.main()
