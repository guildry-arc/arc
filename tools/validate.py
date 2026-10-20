#!/usr/bin/env python3
"""Validate the ARC schemas and examples.

Checks that every schema in schemas/<version>/ is valid JSON Schema (draft 2020-12),
that every file in examples/valid/ passes, and that every file in examples/invalid/ fails.

Example files are named <schema>.<description>.json. For envelope examples, the body is
also validated against the schema selected by the envelope's "type" field.

Usage: python tools/validate.py            (needs: pip install jsonschema)
"""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.5"
SCHEMA_DIR = ROOT / "schemas" / VERSION

schemas = {p.name: json.loads(p.read_text()) for p in sorted(SCHEMA_DIR.glob("*.json"))}
registry = Registry().with_resources(
    (s["$id"], Resource.from_contents(s)) for s in schemas.values()
)

def validator(name):
    return Draft202012Validator(schemas[name], registry=registry, format_checker=FormatChecker())

def errors_for(path):
    return errors_for_named(path, path.name.split(".")[0] + ".json")

def errors_for_named(path, name):
    instance = json.loads(path.read_text())
    errs = [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}"
            for e in validator(name).iter_errors(instance)]
    if name == "envelope.json" and not errs:
        body_schema = instance["type"].split("/", 1)[1] + ".json"
        errs += [f"body/{'/'.join(map(str, e.absolute_path))}: {e.message}"
                 for e in validator(body_schema).iter_errors(instance["body"])]
    return errs

failed = 0
for name, s in schemas.items():
    try:
        Draft202012Validator.check_schema(s)
    except Exception as e:
        failed += 1; print(f"FAIL  schema {name}: {e}")
print(f"ok    {len(schemas)} schemas are valid draft 2020-12")

for kind, should_pass in (("valid", True), ("invalid", False)):
    files = sorted((ROOT / "examples" / kind).glob("*.json"))
    for f in files:
        errs = errors_for(f)
        if bool(errs) == should_pass:
            failed += 1
            print(f"FAIL  {kind}/{f.name}: " + ("; ".join(errs[:3]) if errs else "passed but should fail"))
    print(f"ok    {len(files)} {kind} examples checked")

vec = ROOT / "test-vectors" / "signing" / "receipt-envelope.json"
if vec.exists():
    errs = errors_for_named(vec, "envelope.json")
    if errs: failed += 1; print("FAIL  signed test vector: " + "; ".join(errs[:3]))
    else: print("ok    signed test vector matches the envelope and receipt schemas")

print("READY." if not failed else f"{failed} failure(s)")
sys.exit(1 if failed else 0)
