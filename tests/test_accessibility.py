"""Guard the dashboard's key motion and text-contrast accessibility choices."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def relative_luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045
              else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return sum(weight * channel for weight, channel in zip((0.2126, 0.7152, 0.0722), linear))


def contrast_ratio(foreground, background):
    light, dark = sorted((relative_luminance(foreground), relative_luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


class AccessibilityTests(unittest.TestCase):
    def test_shared_text_colours_meet_wcag_aa_for_their_backgrounds(self):
        self.assertGreaterEqual(contrast_ratio("#52677A", "#F3F6F8"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#17324D", "#FFFFFF"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#E6F0F2", "#102B45"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#80CFC9", "#102B45"), 4.5)

    def test_reduced_motion_preference_disables_nonessential_motion(self):
        css = (ROOT / "src/ui.py").read_text()
        self.assertRegex(css, r"@media\s*\(prefers-reduced-motion:\s*reduce\)")
        reduced_rule = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([^}]+)", css
        )
        self.assertIsNotNone(reduced_rule)
        self.assertIn("animation:none", reduced_rule.group(1).replace(" ", ""))
        self.assertIn("transition:none", reduced_rule.group(1).replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
