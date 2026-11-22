import unittest
from ai_pipeline.nlp.normalizer import normalize_amharic_text
from ai_pipeline.nlp.keywords import detect_hazard_from_amharic_text

class TestAmharicNLP(unittest.TestCase):
    def test_normalization(self):
        self.assertTrue(len(normalize_amharic_text("በከባድ ዝናብ ተራራው ተደርምሶ መንገዱ ተዘግቷል")) > 0)
    def test_keyword_detection(self):
        self.assertEqual(detect_hazard_from_amharic_text("በመንደሩ ውስጥ ትልቅ ናዳ እና የመሬት መደርመስ ተከስቷል"), "HAZ-LANDSLIDE")

if __name__ == "__main__":
    unittest.main()
