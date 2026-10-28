"""Release checks for the new portable skill; behavioral evaluation is separate."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
ROLE = ROOT / 'plugins/coding-engineer-skills'
SKILL = ROLE / 'skills/good-offence'


def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


class DistributionTests(unittest.TestCase):
    def test_single_entry_and_matching_role_inventories(self):
        self.assertEqual([p.relative_to(SKILL).as_posix() for p in SKILL.rglob('SKILL.md')], ['SKILL.md'])
        self.assertEqual(len(list((ROLE/'skills').glob('*/SKILL.md'))), 31)
        for host in ['.codex-plugin', '.claude-plugin']:
            metadata = json.loads((ROLE/host/'plugin.json').read_text())
            self.assertEqual(metadata['version'], '0.2.6')
            self.assertIn('Thirty-one', metadata['description'])
        claude = json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
        self.assertEqual(next(p for p in claude['plugins'] if p['name']=='coding-engineer-skills')['version'], '0.2.6')
        native = json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
        entries = [p for p in native['plugins'] if p['name']=='coding-engineer-skills']
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['source']['path'], './plugins/coding-engineer-skills')

    def test_vendor_text_and_license_notices_keep_original_identities(self):
        expected = {
            'references/upstream/ponytail/ponytail-review-v4.13.0.md':'b92e98304c1d0c101fc5e02aa33c4252f9a8db85',
            'references/upstream/ponytail/LICENSE':'715d483338cea4365f0d91a27799cf61226d6bcf',
            'references/upstream/rob-morris/software-design-review/reviewers/premise.md':'d42aedd321aa914ba34ae8bf2966695b52efb488',
            'references/upstream/rob-morris/software-design-review/reviewers/defensive.md':'cb3fd35b899786092a8260fc06af41f1f73caad2',
            'references/upstream/rob-morris/software-design-review/reference/principles.md':'1e15425ad24728fbf7c1ab6f1cb979a18b6186f5',
            'references/upstream/rob-morris/LICENSE':'cc8d6fb1e3bb22577d82b89affd4fe9baeb3429c',
        }
        for path, sha in expected.items():
            self.assertEqual(blob_sha(SKILL/path), sha, path)
        self.assertEqual((SKILL/'LICENSE').read_bytes(), (ROLE/'LICENSE').read_bytes())
        for filename in ['premise.md', 'defensive.md']:
            path = SKILL/'references/upstream/rob-morris/software-design-review/reviewers'/filename
            self.assertTrue((path.parent/'../reference/principles.md').resolve().is_file())

    def test_public_inputs_do_not_embed_grading_answers_or_machine_state(self):
        suite = json.loads((SKILL/'evals/suite.json').read_text())
        self.assertEqual(len(suite['cases']), 5)
        for index, case in enumerate(suite['cases'], 1):
            self.assertEqual(set(case), {'id','input'})
            self.assertEqual(case['id'], f'case-{index:02d}')
            self.assertTrue((SKILL/'evals'/case['input']).is_file())
        self.assertTrue((SKILL/'evals/expected.json').is_file())
        forbidden = {'run.sh','state.sqlite3','opencode_runner.py','target-repos.md','launchd.plist'}
        for path in SKILL.rglob('*'):
            if path.is_file():
                self.assertNotIn(path.name, forbidden)
                self.assertNotIn(b'/Users/macopc/', path.read_bytes(), path.as_posix())
        self.assertIn('name: good-offence\n', (SKILL/'SKILL.md').read_text())
        self.assertNotIn('allow_implicit_invocation: false', (SKILL/'agents/openai.yaml').read_text())


if __name__ == '__main__':
    unittest.main()
