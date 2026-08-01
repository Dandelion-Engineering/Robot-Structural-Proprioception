"""Contract tests for the shared Protocol-P primitives in ``utils/protocol_p.py``.

The module carries three things every Protocol-P script must agree on: the two hash
domains, the two text-domain pins, and CANONICAL_JSON.  Its correctness properties are
therefore mostly *sameness* properties -- there must be one implementation and one copy
of each pin -- plus one dependency property that only exists because of why the module
was created.

Until Session 51 those names lived in the replay gate, and importing them made Stage 0
a transitive importer of ``mujoco`` through the gate's import of the generator.  The
subprocess tests below pin the fix: they run in a fresh interpreter, because
``sys.modules`` in this one is already polluted by every other test in the suite, and a
same-process check would report whatever some earlier import happened to load.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

import analyze_synchronous_difference_null as stage_0  # noqa: E402
import protocol_p_replay_gate as gate  # noqa: E402
from utils import protocol_p as shared  # noqa: E402

PROTOCOL_PATH = PACKET_ROOT / "protocol" / shared.PROTOCOL_FILENAME
ASSIGNMENT_PATH = PACKET_ROOT / "config" / shared.ASSIGNMENT_FILENAME


def _fresh_interpreter(snippet: str) -> str:
    """Run ``snippet`` in a fresh ``-B`` interpreter and return its stripped stdout.

    Inputs: a Python source string. Outputs: its stdout. Purpose: a dependency question
    is only answerable in a process that has imported nothing else; ``-B`` also keeps
    the run from writing bytecode into the packet tree.
    """

    proc = subprocess.run(
        [sys.executable, "-B", "-c", snippet],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS_ROOT),
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"probe interpreter failed with status {proc.returncode}:\n{proc.stderr}"
        )
    return proc.stdout.strip()


# ---------------------------------------------------------------------------
# The pins are the real files' digests
# ---------------------------------------------------------------------------


def test_the_protocol_pin_is_this_protocol_file() -> None:
    """The pinned text digest must be the digest of the protocol file on disk."""

    assert PROTOCOL_PATH.is_file()
    assert shared.canonical_text_sha256(PROTOCOL_PATH) == shared.PROTOCOL_CANONICAL_SHA256


def test_the_assignment_pin_is_the_approved_assignment_file() -> None:
    """The pinned text digest must be the digest of the approved assignment."""

    assert ASSIGNMENT_PATH.is_file()
    assert (
        shared.canonical_text_sha256(ASSIGNMENT_PATH) == shared.ASSIGNMENT_CANONICAL_SHA256
    )


# ---------------------------------------------------------------------------
# One implementation, one copy of each pin
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "ProtocolPError",
        "canonical_text_sha256",
        "PROTOCOL_FILENAME",
        "PROTOCOL_CANONICAL_SHA256",
        "ASSIGNMENT_FILENAME",
        "ASSIGNMENT_CANONICAL_SHA256",
    ],
)
def test_the_gate_and_stage_0_share_one_object(name: str) -> None:
    """Both consumers must bind the *same* object, not an equal copy.

    A second copy of a pinned digest is a second thing to forget to update, and a
    second ``ProtocolPError`` class would make ``except ProtocolPError`` in one script
    silently fail to catch the other's failure.
    """

    assert getattr(gate, name) is getattr(shared, name)
    assert getattr(stage_0, name) is getattr(shared, name)


def test_both_consumers_share_one_fail_loud_helper() -> None:
    """``_require`` in either consumer is the shared ``require``, bound privately."""

    assert gate._require is shared.require
    assert stage_0._require is shared.require


def test_stage_0_shares_the_canonical_json_rule() -> None:
    """CANONICAL_JSON must have exactly one implementation across the protocol."""

    assert stage_0.canonical_json is shared.canonical_json


def test_the_binary_pins_stay_with_the_check_that_reads_them() -> None:
    """The two ``.npz`` pins belong to the replay gate, not to the shared module.

    Section 7 is the only consumer that reads them. Keeping a pin next to the check
    that enforces it is what makes an unused pin visible as unused.
    """

    for name in (
        "PLANT_REFERENCE_RAW_SHA256",
        "OBSERVATION_REFERENCE_RAW_SHA256",
        "PLANT_REFERENCE_TEXT_FOLDED_SHA256",
        "OBSERVATION_REFERENCE_TEXT_FOLDED_SHA256",
    ):
        assert hasattr(gate, name)
        assert not hasattr(shared, name)


# ---------------------------------------------------------------------------
# The dependency property the extraction exists to create
# ---------------------------------------------------------------------------


def test_the_shared_module_itself_imports_only_the_standard_library() -> None:
    """Loaded by path, outside its package, the module pulls in neither MuJoCo nor NumPy.

    Loading by path is the instrument that answers the question actually asked. Importing
    ``utils.protocol_p`` the ordinary way first executes ``utils/__init__.py``, which
    re-exports ``SCHEMA_VERSION`` from ``utils.schema_types`` and therefore imports NumPy
    -- a property of the package, not of this module. The next test pins that split so
    neither claim can be mistaken for the other.
    """

    result = _fresh_interpreter(
        "import sys, importlib.util\n"
        "spec = importlib.util.spec_from_file_location('protocol_p_standalone', r'%s')\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        "print('mujoco' in sys.modules, 'numpy' in sys.modules)\n"
        % (SCRIPTS_ROOT / "utils" / "protocol_p.py")
    )
    assert result == "False False"


def test_the_utils_package_init_is_what_pulls_numpy_in() -> None:
    """Through the package the shared module costs NumPy -- and still never MuJoCo.

    Recorded as a test rather than as a remark because the two facts are easy to
    conflate: the protocol's primitives depend on nothing, while any ``from utils import
    ...`` costs NumPy through the package's own re-export.
    """

    result = _fresh_interpreter(
        "import sys; sys.path.insert(0, r'%s')\n"
        "from utils import protocol_p\n"
        "print('mujoco' in sys.modules, 'numpy' in sys.modules)\n" % SCRIPTS_ROOT
    )
    assert result == "False True"


def test_stage_0_does_not_import_mujoco() -> None:
    """Stage 0 constructs no mechanics, so importing it must not import MuJoCo.

    Session 50 measured the opposite and the packet runbook and public log both had to
    be corrected. The claim is now machine-checked rather than reasoned about: this test
    goes red the moment Stage 0 acquires a transitive plant dependency again.
    """

    result = _fresh_interpreter(
        "import sys; sys.path.insert(0, r'%s')\n"
        "import analyze_synchronous_difference_null\n"
        "print('mujoco' in sys.modules)\n" % SCRIPTS_ROOT
    )
    assert result == "False"


def test_the_replay_gate_still_imports_the_plant() -> None:
    """The gate rebuilds a reservation, so its MuJoCo import is intrinsic, not a slip.

    Stated as a test so the asymmetry is recorded: the extraction removed an
    *incidental* dependency from Stage 0 and left an *intrinsic* one where it belongs.
    """

    result = _fresh_interpreter(
        "import sys; sys.path.insert(0, r'%s')\n"
        "import protocol_p_replay_gate\n"
        "print('mujoco' in sys.modules)\n" % SCRIPTS_ROOT
    )
    assert result == "True"


# ---------------------------------------------------------------------------
# CANONICAL_JSON
# ---------------------------------------------------------------------------


def test_canonical_json_sorts_keys_and_omits_whitespace() -> None:
    """Two payloads differing only in key order must serialize identically."""

    assert shared.canonical_json({"b": 1, "a": 2}) == shared.canonical_json({"a": 2, "b": 1})
    assert shared.canonical_json({"a": 2, "b": 1}) == '{"a":2,"b":1}'


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_canonical_json_refuses_non_finite_floats(value: float) -> None:
    """``allow_nan=False`` is load-bearing: plain ``json.dumps`` would emit ``NaN``."""

    with pytest.raises(ValueError):
        shared.canonical_json({"value": value})
