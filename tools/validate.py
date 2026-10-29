#!/usr/bin/env python3
"""Validate the ARC schemas and examples.

Checks that every schema in schemas/<version>/ is valid JSON Schema (draft 2020-12),
that every file in examples/valid/ passes the current version's schemas, and that every
file in examples/invalid/ fails them.

Example files are named <schema>.<description>.json. For envelope examples, the body is
also validated against the schema selected by the envelope's "type" field.

Backward compatibility (SPEC.md §18.6): every valid example frozen in
test-vectors/compat/<older>/ must validate under its own version's schemas AND under the
current version's schemas. Signed vectors are validated under the version their envelope
declares (§18.5).

Usage: python tools/validate.py            (needs: pip install jsonschema)
"""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.7"

schema_sets = {
    d.name: {p.name: json.loads(p.read_text()) for p in sorted(d.glob("*.json"))}
    for d in sorted((ROOT / "schemas").iterdir()) if d.is_dir()
}
registry = Registry().with_resources(
    (s["$id"], Resource.from_contents(s)) for ss in schema_sets.values() for s in ss.values()
)

def validator(version, name):
    return Draft202012Validator(schema_sets[version][name], registry=registry, format_checker=FormatChecker())

def errors_for(path, version=VERSION, name=None):
    name = name or path.name.split(".")[0] + ".json"
    instance = json.loads(path.read_text())
    errs = [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}"
            for e in validator(version, name).iter_errors(instance)]
    if name == "envelope.json" and not errs:
        body_schema = instance["type"].split("/", 1)[1] + ".json"
        errs += [f"body/{'/'.join(map(str, e.absolute_path))}: {e.message}"
                 for e in validator(version, body_schema).iter_errors(instance["body"])]
    return errs

failed = 0
for version, ss in schema_sets.items():
    for name, s in ss.items():
        try:
            Draft202012Validator.check_schema(s)
        except Exception as e:
            failed += 1; print(f"FAIL  schema {version}/{name}: {e}")
    print(f"ok    {len(ss)} schemas in {version}/ are valid draft 2020-12")

for kind, should_pass in (("valid", True), ("invalid", False)):
    files = sorted((ROOT / "examples" / kind).glob("*.json"))
    for f in files:
        errs = errors_for(f)
        if bool(errs) == should_pass:
            failed += 1
            print(f"FAIL  {kind}/{f.name}: " + ("; ".join(errs[:3]) if errs else "passed but should fail"))
    print(f"ok    {len(files)} {kind} examples checked against {VERSION}")

compat = ROOT / "test-vectors" / "compat"
for d in sorted(p for p in compat.iterdir() if p.is_dir()) if compat.exists() else []:
    files = sorted(d.glob("*.json"))
    for f in files:
        for v in (d.name, VERSION):
            errs = errors_for(f, v)
            if errs:
                failed += 1; print(f"FAIL  compat/{d.name}/{f.name} under {v}: " + "; ".join(errs[:3]))
    print(f"ok    {len(files)} arc/{d.name} vectors validate under {d.name} and {VERSION}")

vec = ROOT / "test-vectors" / "signing" / "receipt-envelope.json"
if vec.exists():
    declared = json.loads(vec.read_text())["arc"]
    for v in dict.fromkeys((declared, VERSION)):
        errs = errors_for(vec, v, "envelope.json")
        if errs: failed += 1; print(f"FAIL  signed test vector under {v}: " + "; ".join(errs[:3]))
    print(f"ok    signed arc/{declared} test vector matches the envelope and receipt schemas ({declared} and {VERSION})")

print("READY." if not failed else f"{failed} failure(s)")
sys.exit(1 if failed else 0)
