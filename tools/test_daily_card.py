"""Run with: python -B -m unittest discover -s tools -p 'test_daily_card.py'."""
import copy
import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


class DailyCardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name('render_daily_card.py')
        if not path.exists():
            raise AssertionError('The daily card renderer has not been implemented')
        spec = importlib.util.spec_from_file_location('daily_card', path)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.scratch = Path(__file__).resolve().parents[1] / 'workspace' / 'daily-cards' / '.test-output'
        cls.scratch.mkdir(parents=True, exist_ok=True)

    def sample(self):
        return {'date': '2026-10-21', 'title': '청크와 벡터',
                'summary': '청크와 같은 위치의 벡터를 함께 저장한다.',
                'sections': [{'title': 'Point 구성', 'body': ['ID와 벡터, 원문을 연결한다.'],
                              'visual': {'type': 'compare', 'items': [
                                  {'label': 'vector', 'detail': '검색', 'icon': 'vector'},
                                  {'label': 'payload', 'detail': '원문', 'icon': 'document'}]},
                              'verification': {'claim': '검색용 벡터와 원문 payload의 역할 구분',
                                               'sources': [{'title': 'Qdrant Points', 'url': 'https://qdrant.tech/documentation/concepts/points/'}]}}],
                'verification': {'status': 'verified', 'checked_at': '2026-10-22'},
                'remember': '원문과 벡터의 순서를 맞춘다.',
                'sources': [{'kind': 'project', 'title': '학습 글', 'ref': '_posts/example.md'}]}

    def test_wrap_preserves_hangul_and_long_identifiers_without_overflow(self):
        font = self.mod.load_font(48)
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        original = '한글과 긴 문장을 읽기 좋게 나눈다. normalize_embeddings=True와긴연속문자열'*3
        lines = self.mod.wrap_text(original, font, 420)
        self.assertEqual(''.join(original.split()), ''.join(''.join(lines).split()))
        self.assertGreater(len(lines), 3)
        self.assertTrue(all(draw.textlength(line, font=font) <= 420 for line in lines))

    def test_more_content_extends_canvas_and_keeps_width(self):
        with tempfile.TemporaryDirectory(dir=self.scratch) as directory:
            short = self.sample()
            long = copy.deepcopy(short)
            long['sections'] *= 8
            a, b = Path(directory)/'short.png', Path(directory)/'long.png'
            self.mod.render_card(short, a)
            self.mod.render_card(long, b)
            with Image.open(a) as first, Image.open(b) as second:
                self.assertEqual(first.format, 'PNG')
                self.assertEqual(first.width, 1080)
                self.assertEqual(second.width, 1080)
                self.assertGreater(second.height, first.height + 1000)
                self.assertEqual(second.mode, 'RGB')

    def test_invalid_or_empty_record_does_not_create_image(self):
        with tempfile.TemporaryDirectory(dir=self.scratch) as directory:
            for field, value in [('date', '2026-02-30'), ('sections', []), ('sources', []), ('summary', '')]:
                data = self.sample()
                data[field] = value
                output = Path(directory)/'invalid.png'
                with self.assertRaises(ValueError):
                    self.mod.render_card(data, output)
                self.assertFalse(output.exists())

    def test_unverified_concept_or_missing_diagram_is_rejected(self):
        for defect in ['unverified', 'missing_visual', 'missing_evidence']:
            data = self.sample()
            if defect == 'unverified':
                data['verification']['status'] = 'pending'
            elif defect == 'missing_visual':
                del data['sections'][0]['visual']
            else:
                data['sections'][0]['verification']['sources'] = []
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                self.mod.validate(data)

    def test_page_preparation_rejects_text_changed_after_image_upload(self):
        from prepare_daily_card_page import prepare
        with tempfile.TemporaryDirectory(dir=self.scratch) as directory:
            folder=Path(directory)
            (folder/'card.json').write_text(json.dumps(self.sample()),encoding='utf-8')
            (folder/'upload.json').write_text(json.dumps({'image_sha256':'same-image','suggested_markdown':'image'}),encoding='utf-8')
            (folder/'render.json').write_text(json.dumps({'image_sha256':'same-image','data_sha256':'old-content','visual_reviewed':True}),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'changed'):
                prepare(folder)


if __name__ == '__main__':
    unittest.main()
