"""The SRL pass must read real entity fields and write through the profile store.

Guards the wiring, not the scoring: a block that matches a field nobody sets
still passes every test in ``test_srl_model.py``.
"""

import asyncio

import pytest

from deeptutor.services.memory.consolidator.modes.update import _update_srl_profile
from deeptutor.services.memory.snapshot.entity import Entity
from deeptutor.services.memory.srl import ModeloEstudianteSRL


def _entity(label: str, metadata: dict) -> Entity:
    return Entity(id="e1", label=label, ts="2026-01-01T00:00:00", content="", metadata=metadata)


@pytest.fixture
def learner(monkeypatch):
    """A learner account whose profile the SRL pass can read and write."""
    from deeptutor.multi_user import identity

    store: dict = {"profile": {"age": 9}}
    monkeypatch.setattr(identity, "get_learner_profile", lambda _u: store["profile"])
    monkeypatch.setattr(
        identity, "set_learner_profile", lambda _u, p: store.__setitem__("profile", p) or p
    )
    return store


def test_interaction_event_updates_the_stored_profile(learner):
    entities = [
        _entity(
            "cualquier titulo",
            {
                "srl_action": True,
                "event_type": "abandono_ejercicio",
                "details": "salta_al_primer_error",
            },
        )
    ]

    asyncio.run(_update_srl_profile("alumno", entities, ModeloEstudianteSRL))

    srl = learner["profile"]["srl_profile"]
    # The evasive behaviour drops effort regulation to its floor.
    assert srl["variables"]["v69_regulacion_esfuerzo"] == 1.0
    assert srl["nivel_srl"] == "Medio"  # one variable moved, average barely shifts
    assert srl["nivel_con"] == "Medio"  # no graded attempts yet -> unknown
    assert srl["estrategia_andamiaje"] == "Medio (Facilitador)"


def test_graded_attempts_drive_the_knowledge_level(learner):
    entities = [
        _entity("quiz", {"assessment_attempts": [{"is_correct": True}, {"is_correct": True}]})
    ]

    asyncio.run(_update_srl_profile("alumno", entities, ModeloEstudianteSRL))

    srl = learner["profile"]["srl_profile"]
    assert srl["nivel_con"] == "Alto"
    # matrix row = CON, column = ARR: Alto CON with neutral ARR -> low scaffolding.
    assert srl["estrategia_andamiaje"] == "Bajo (Desafíos Autónomos)"


def test_entities_without_srl_signals_leave_the_profile_alone(learner):
    before = dict(learner["profile"])

    asyncio.run(
        _update_srl_profile(
            "alumno", [_entity("nota normal", {"doc_id": "x"})], ModeloEstudianteSRL
        )
    )

    assert learner["profile"] == before
