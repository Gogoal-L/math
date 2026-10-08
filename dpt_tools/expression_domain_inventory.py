"""Inventory EVERY inverse in the original rational-expression AST.

Numerical evaluation may stop at an undefined inverse, so this module
reports the remaining (unreached) inverse nodes without pretending that
they were checked. Unique AST paths are the identity; labels need not be.
"""
from __future__ import annotations


def enumerate_inverse_occurrences(node, path="$") -> list[dict]:
    if not isinstance(node, dict) or "op" not in node:
        raise ValueError(f"invalid expression at {path}")
    op = node["op"]
    out = []
    if op == "inv":
        out.append({"path": path, "label": str(node.get("label", "<unlabeled inverse>"))})
    if "arg" in node:
        out.extend(enumerate_inverse_occurrences(node["arg"], path + ".arg"))
    if "args" in node:
        if not isinstance(node["args"], list):
            raise ValueError(f"args must be a list at {path}")
        for i, child in enumerate(node["args"]):
            out.extend(enumerate_inverse_occurrences(child, f"{path}.args[{i}]"))
    return out


def coverage(inventory: list[dict], sample_ids: list[str], inverse_log: list[dict]) -> list[dict]:
    looked_up = {(entry["sample_id"], entry["node_path"]): entry for entry in inverse_log}
    result = []
    for sid in sample_ids:
        for obj in inventory:
            entry = looked_up.get((sid, obj["path"]))
            if entry is None:
                status = "NOT_REACHED_DEPENDENCY"
            elif entry["defined"]:
                status = "DEFINED"
            elif entry["kind"] == "scalar":
                status = "SINGULAR" if float(entry["abs_value"]) == 0 else "NUMERICALLY_ILL_CONDITIONED"
            else:
                status = "SINGULAR" if float(entry["min_singular_value"]) == 0 else "NUMERICALLY_ILL_CONDITIONED"
            result.append({"sample_id": sid, "path": obj["path"],
                           "label": obj["label"], "status": status})
    return result


def complete_coverage(rows: list[dict]) -> bool:
    return all(row["status"] != "NOT_REACHED_DEPENDENCY" for row in rows)
