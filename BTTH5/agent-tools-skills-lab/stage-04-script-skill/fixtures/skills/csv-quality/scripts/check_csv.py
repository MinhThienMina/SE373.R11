#!/usr/bin/env python3
"""Check task CSV quality and compute workload by owner."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict

REQUIRED_COLUMNS = ("task_id", "owner", "hours")
REASON_ORDER = ("wrong_field_count", "missing_task_id", "duplicate_id", "missing_owner", "invalid_hours")


class InputError(Exception):
    pass


def parse_hours(raw: str | None) -> float | None:
    if raw is None or not raw.strip():
        return None
    try:
        value = float(raw.strip())
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return value


def parse_max_hours(raw: str) -> float:
    value = parse_hours(raw)
    if value is None:
        raise argparse.ArgumentTypeError("--max-hours phai la so huu han khong am.")
    return value


def _issue(line: int, column: str | None, issue_type: str, task_id: str | None, message: str, **extra) -> dict:
    data = {"line": line, "column": column, "type": issue_type, "task_id": task_id, "message": message}
    data.update(extra)
    return data


def analyze(path: str, max_hours: float) -> dict:
    try:
        handle = open(path, encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise InputError(f"Khong doc duoc file {path}: {exc.strerror or exc}") from exc

    with handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next(reader, None)
            if header is None:
                raise InputError(f"File {path} rong, khong co header.")
            columns = [c.strip() for c in header]
            missing = [c for c in REQUIRED_COLUMNS if c not in columns]
            if missing:
                raise InputError(f"Thieu cot bat buoc: {', '.join(missing)}. Header hien co: {', '.join(columns)}")
            index = {name: columns.index(name) for name in REQUIRED_COLUMNS}

            row_count = 0
            missing_owner = 0
            invalid_hours = 0
            first_seen: dict[str, int] = {}
            duplicate_ids: list[str] = []
            issues: list[dict] = []
            excluded_rows: list[dict] = []
            hours_by_owner: dict[str, float] = defaultdict(float)

            for row in reader:
                line = reader.line_num
                if not any(cell.strip() for cell in row):
                    continue
                row_count += 1

                def cell(name: str) -> str:
                    position = index[name]
                    return row[position].strip() if position < len(row) else ""

                task_id = cell("task_id")
                owner = cell("owner")
                hours_text = cell("hours")
                parsed_hours = parse_hours(hours_text)
                reasons: list[str] = []

                if len(row) != len(columns):
                    reasons.append("wrong_field_count")
                    issues.append(_issue(line, None, "wrong_field_count", task_id or None, f"Co {len(row)} truong, header co {len(columns)} cot."))
                if not task_id:
                    reasons.append("missing_task_id")
                    issues.append(_issue(line, "task_id", "missing_task_id", None, "task_id trong."))
                elif task_id in first_seen:
                    reasons.append("duplicate_id")
                    if task_id not in duplicate_ids:
                        duplicate_ids.append(task_id)
                    issues.append(_issue(line, "task_id", "duplicate_id", task_id, f"task_id {task_id} da xuat hien o line {first_seen[task_id]}."))
                else:
                    first_seen[task_id] = line
                if not owner:
                    reasons.append("missing_owner")
                    missing_owner += 1
                    issues.append(_issue(line, "owner", "missing_owner", task_id or None, "owner trong."))
                if parsed_hours is None:
                    reasons.append("invalid_hours")
                    invalid_hours += 1
                    issues.append(_issue(line, "hours", "invalid_hours", task_id or None, f"hours '{hours_text}' khong phai so huu han khong am.", value=hours_text))

                if reasons:
                    ordered = [reason for reason in REASON_ORDER if reason in reasons]
                    excluded_rows.append({"line": line, "task_id": task_id or None, "reasons": ordered})
                else:
                    hours_by_owner[owner] += parsed_hours
        except csv.Error as exc:
            raise InputError(f"Loi parse CSV o line {reader.line_num}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise InputError(f"File {path} khong phai UTF-8: {exc}") from exc

    normalized_hours = dict(sorted(hours_by_owner.items()))
    overloaded = [{"owner": owner, "total_hours": total} for owner, total in normalized_hours.items() if total > max_hours]
    return {
        "input": path,
        "row_count": row_count,
        "missing_owner_count": missing_owner,
        "invalid_hours_count": invalid_hours,
        "duplicate_id_count": len(duplicate_ids),
        "duplicate_ids": duplicate_ids,
        "issues": sorted(issues, key=lambda item: item["line"]),
        "max_hours": max_hours,
        "hours_by_owner": normalized_hours,
        "overloaded_owners": overloaded,
        "excluded_rows": excluded_rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kiem tra CSV cong viec va tinh tong gio theo owner.")
    parser.add_argument("--input", required=True, help="Duong dan CSV, vi du data/tasks.csv")
    parser.add_argument("--max-hours", required=True, type=parse_max_hours, help="Nguong gio huu han khong am")
    args = parser.parse_args(argv)
    try:
        result = analyze(args.input, args.max_hours)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
