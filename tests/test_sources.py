import csv
import hashlib
import json
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'data'


def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def rows(name):
    with (DATA / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def digest(name):
    return hashlib.sha256((DATA / name).read_bytes()).hexdigest()


class SourceContract(unittest.TestCase):
    def test_producer_material(self):
        manifest = load('old-cut.json')
        for chunk in manifest['files']:
            assert digest(chunk['file']) == chunk['sha256']
            assert all(chunk['begin'] <= row['reading'] < chunk['end'] for row in rows(chunk['file']))
        journal = load('journal.json')
        assert journal[0][:2] == ['old', 89] and journal[3][:2] == ['old', 88]
        assert journal[-6:-3] == journal[-3:]
        assert load('handoff.json')['new_cut_tx'] == load('new-cut.json')['cut']
        for chunk in load('new-cut.json')['files']:
            assert digest(chunk['file']) == chunk['sha256']
