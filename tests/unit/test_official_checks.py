import csv
import pytest
from tennis_lab.ingestion.audit import official_checks


def test_official_walkover_detects_inverted_winner(tmp_path):
    columns = ['tourney_id', 'round', 'winner_name', 'loser_name', 'score']
    for source in ('sackmann', 'tml'):
        directory = tmp_path / source
        directory.mkdir()
        name = 'atp_matches_2024.csv' if source == 'sackmann' else '2024.csv'
        winner, loser = ('Jan Lennard Struff', 'Corentin Moutet') if source == 'sackmann' else ('Corentin Moutet', 'Jan-Lennard Struff')
        with (directory / name).open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerow(dict(zip(columns, ['2024-0096', 'R32', winner, loser, 'W/O'])))
    checks = [{'season': 2024, 'tournament_code': '96', 'round': 'R32',
               'winner_name': 'Corentin Moutet', 'loser_name': 'Jan Lennard Struff',
               'score': 'W/O', 'source_url': 'https://www.atptour.com/official-check'}]
    results = official_checks(tmp_path, checks, 2024)
    assert results[0]['passed'] is False
    assert results[1]['passed'] is True


def test_official_checks_cannot_use_evaluation_year_outcomes(tmp_path):
    with pytest.raises(ValueError, match='evaluación'):
        official_checks(tmp_path, [{'season': 2025}], 2024)
