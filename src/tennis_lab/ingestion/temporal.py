"""Disponibilidad conservadora; una fecha de torneo nunca sustituye evidencia."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class ResultTiming:
    completed_on: date | None
    event_timezone: str

    @property
    def usable_from(self) -> datetime | None:
        zone = ZoneInfo(self.event_timezone)
        if self.completed_on is None:
            return None
        next_day = self.completed_on + timedelta(days=1)
        return datetime.combine(next_day, time.min, zone).astimezone(timezone.utc)

    def known_before(self, prediction_at: datetime) -> bool:
        if prediction_at.tzinfo is None or prediction_at.utcoffset() is None:
            raise ValueError("La predicción necesita una zona horaria")
        usable = self.usable_from
        return usable is not None and usable <= prediction_at

    def training_eligible(self, source_season: int, cutoff: date) -> bool:
        # Año de temporada y disponibilidad son condiciones independientes.
        # Corte inclusivo por fecha UTC; instante exclusivo: 1 de enero siguiente.
        boundary = datetime.combine(cutoff + timedelta(days=1), time.min, timezone.utc)
        usable = self.usable_from
        return (source_season <= cutoff.year and self.completed_on is not None
                and self.completed_on <= cutoff and usable is not None and usable < boundary)
