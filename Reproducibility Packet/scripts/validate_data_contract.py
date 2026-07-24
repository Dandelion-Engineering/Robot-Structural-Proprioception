"""Validate the machine schema, config lifecycle, manifest, and suite storage.

The config check is always run. Manifest and observation-root checks are
optional so the foundation can be verified before the jointly-approved Gate-3
manifest exists. Use ``--require-frozen`` only for confirmatory operations.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from utils.config_contract import load_config
from utils.storage_contract import (
    DeployableObservationLoader,
    audit_identity_manifest,
    read_identity_manifest,
)


def parse_args() -> argparse.Namespace:
    """Parse portable contract-validation arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, required=True, help="Machine schema.json path.")
    parser.add_argument("--config", type=Path, required=True, help="Draft or frozen config path.")
    parser.add_argument(
        "--require-frozen",
        action="store_true",
        help="Reject draft/dev state; required for confirmatory operations.",
    )
    parser.add_argument("--manifest", type=Path, help="Optional identity manifest.csv.")
    parser.add_argument(
        "--suite-root",
        type=Path,
        help="Optional single deployable root: <run-root>/observations/<suite>.",
    )
    parser.add_argument("--suite", choices=("C0", "C1", "S"), help="Suite for --suite-root.")
    parser.add_argument(
        "--require-complete-c1-s-pairs",
        action="store_true",
        help="Require every manifest pair to include both C1 and S.",
    )
    return parser.parse_args()


def main() -> int:
    """Run selected fail-loud contract checks and print concise audit counts."""

    args = parse_args()
    if (args.suite_root is None) != (args.suite is None):
        raise ValueError("--suite-root and --suite must be supplied together")
    config = load_config(args.config, args.schema, require_frozen=args.require_frozen)
    print(
        f"Config OK: status={config.status}, config_hash={config.config_hash}, "
        f"confirmatory={config.is_frozen}",
        flush=True,
    )
    if args.manifest is not None:
        rows = read_identity_manifest(args.manifest)
        counts = audit_identity_manifest(
            rows,
            expected_config=config,
            require_complete_c1_s_pairs=args.require_complete_c1_s_pairs,
        )
        print(f"Identity manifest OK: {counts}", flush=True)
    if args.suite_root is not None:
        loader = DeployableObservationLoader(
            args.suite_root,
            args.suite,
            config,
            require_frozen=args.require_frozen,
        )
        print(
            f"Observation storage OK: suite={loader.suite}, counts={loader.audit_all()}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
