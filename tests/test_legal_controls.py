from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LegalContainmentTestCase(unittest.TestCase):
    def test_review_hold_pages_do_not_republish_withdrawn_operational_text(self) -> None:
        held = {
            "field/ew-countermeasures.md": ("Publication Hold", "hunter-killer"),
            "field/intercept-ops.md": ("Publication Hold", "full throttle through impact"),
            "field/elint-operators.md": ("Publication Hold", "vector an interceptor"),
            "components/military-firmware-forks.md": ("Publication Hold", "CIAJeepDoors"),
            "components/remote-id-custom-builds.md": ("Accuracy Hold", "set drone_serial"),
            "components/ndaa-compliance.md": ("Accuracy Hold", "FOCI test clean"),
            "components/orqa-hardware-guide.md": ("Review Hold", "Standard EAR99 classification"),
            "integration/wingman-apb.md": ("Review Hold", "2.3 TOPS NPU"),
        }

        for relative, (required, forbidden) in held.items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(required, text)
                self.assertNotIn(forbidden, text)
                self.assertIn("jeremiah@midwestniceuas.com", text)

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
