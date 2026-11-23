#!/usr/bin/env python3
"""Check immutable source provenance and regenerate the source-to-workstream index.

This is a specification consistency check, not an ERP acceptance test. It never
sets a business test to passed. Run --write after reviewing source/mapping changes.
"""
import argparse
import hashlib
import json
import re
import runpy
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE = DOCS / "erp-source"
REQUIRED = [
    "00_Original_Requirements.md", "00_Project_Standards.md",
    "01_Phase_1_Foundation.md", "02_Phase_2_Master_Data.md",
    "03_Phase_3_Inventory.md", "04_Phase_4_Purchases_and_Sales.md",
    "05_Phase_5_Accounting.md", "06_Phase_6_Manufacturing.md",
    "07_Phase_7_Reports_and_Analytics.md", "08_Phase_8_Testing_and_Optimization.md",
]
EXPECTED_ROLES = ["Super Admin", "Admin", "Accountant", "Sales Manager",
                  "Purchase Manager", "Inventory Manager", "Production Manager", "Cashier", "Viewer"]
PROFILES = {
    "foundation": {
        "screens": "Login, protected layout, users, roles, business settings",
        "code": "backend/app/auth; backend/app/modules/users; backend/app/modules/roles; backend/app/modules/settings; backend/app/modules/accounting/posting.py",
        "contracts": "docs/api.md#implemented-routes; docs/openapi.json",
        "database": "Implemented: businesses, business_settings, users, roles, permissions, user_roles, role_permissions, auth_sessions, audit_logs, document_sequences, idempotency_records, accounts, journal_entries, journal_entry_lines",
        "evidence": "docs/phases/phase-01-foundation.md; backend/tests/integration/test_stage1.py; backend/tests/test_security.py; backend/tests/test_foundation.py",
        "status": "Foundation evidence recorded previously; source additions and API differences still require reconciliation",
    },
    "master": {
        "screens": "Master data workspace: catalog, units/conversions, parties, warehouses, opening-balance drafts",
        "code": "frontend/src/workspaces/catalog.json; backend services not implemented",
        "contracts": "erp-source/02_Phase_2_Master_Data.md#proposed-apis",
        "database": "Planned Phase 2 tables: products, units, product_unit_conversions, categories, brands, manufacturers, warehouses, product_images, product_suppliers, parties, party_roles, party_contacts, party_addresses, customer_profiles, supplier_profiles, vendor_profiles, opening_balance_drafts",
        "evidence": "Required M01–M09; no persisted master-data acceptance evidence",
        "status": "UI scaffold; business APIs, migrations and verification pending",
    },
    "inventory": {
        "screens": "Inventory workspace: stock, movements, openings, damage, reservations, transfers, counts, valuation, batches, alerts",
        "code": "frontend/src/workspaces/catalog.json; backend/app/modules/inventory/service.py is an interface only",
        "contracts": "erp-source/03_Phase_3_Inventory.md#proposed-apis",
        "database": "Planned Phase 3 tables: inventory_transactions, inventory_movements, stock_balances, stock_reservations, batches, batch_stock_balances, stock_transfers, stock_transfer_lines, stock_counts, stock_count_lines, inventory_cost_layers or inventory_cost_state, alert_rules, alert_events",
        "evidence": "Required I01–I11; no stock movement/valuation acceptance evidence",
        "status": "UI scaffold and service interface; implementation and verification pending",
    },
    "trade": {
        "screens": "Purchase and Sales workspaces: orders, receiving, matching, invoices, POS, settlements, returns",
        "code": "frontend/src/workspaces/catalog.json; backend services not implemented",
        "contracts": "erp-source/04_Phase_4_Purchases_and_Sales.md#proposed-apis",
        "database": "Planned Phase 4 tables: purchase_orders/lines, goods_receipts/lines, supplier_invoices/lines, receipt_invoice_matches, sales_invoices/lines, sales_allocations, payment_methods, payments, payment_allocations, sales_returns/lines, purchase_returns/lines, credit_notes, debit_notes, document_taxes, document_charges",
        "evidence": "Required T01–T15; no persisted sales/purchase/payment acceptance evidence",
        "status": "UI scaffold; business APIs, migrations and verification pending",
    },
    "accounting": {
        "screens": "Accounting workspace: accounts, journals, books/ledgers, AR/AP, expenses, allocations, reconciliation, periods and statements",
        "code": "backend/app/modules/accounting/posting.py (internal kernel); frontend/src/workspaces/catalog.json",
        "contracts": "erp-source/05_Phase_5_Accounting.md#proposed-apis; docs/api.md (internal kernel is not an HTTP journal workflow)",
        "database": "Implemented: accounts, journal_entries, journal_entry_lines; planned: account_mappings, fiscal_periods, cash_bank_accounts, payments/allocations, expense_categories, expenses/attachments, bank_statement_imports/lines, reconciliation_sessions/matches, cash_closings, reminder_rules/deliveries",
        "evidence": "backend/tests/integration/test_stage1.py verifies kernel only; required A01–A10 full accounting evidence pending",
        "status": "Posting kernel verified previously; accounting workflows and reports pending",
    },
    "manufacturing": {
        "screens": "Manufacturing workspace: BOMs, schedules, orders, consumption, output, labor/overhead, waste/rework, quality, costs, genealogy",
        "code": "frontend/src/workspaces/catalog.json; backend services not implemented",
        "contracts": "erp-source/06_Phase_6_Manufacturing.md#proposed-apis",
        "database": "Planned Phase 6 tables: bills_of_materials, bom_versions/lines, production_schedules/exceptions, manufacturing_orders/lines, production_records, material_consumptions/lines, production_outputs, production_labor_costs, production_overheads, quality_checks/results, batch_genealogy",
        "evidence": "Required P01–P12; no production/WIP/genealogy acceptance evidence",
        "status": "UI scaffold; business APIs, migrations and verification pending",
    },
    "reports": {
        "screens": "Dashboard and 40 named report routes; see report-catalog.json and report-verification.md",
        "code": "frontend/src/pages/DashboardPage.jsx; frontend/src/pages/workspaces/ResourcePage.jsx; backend aggregation/export services not implemented",
        "contracts": "erp-source/07_Phase_7_Reports_and_Analytics.md#proposed-apis; report-catalog.json",
        "database": "Planned reads of posted movements, journals, documents, allocations, genealogy; report_export_jobs/files are not migrated",
        "evidence": "R01.01–R01.40 each have six explicit verification cases; R02–R08 also required; all business results pending",
        "status": "Exact source catalog reconciled; totals, permissions, drill-downs, history and exports not verified",
    },
    "ui": {
        "screens": "All workspace routes; shared forms, tables, dialogs, charts, filters, theme/navigation",
        "code": "frontend/src/components; frontend/src/forms; frontend/src/hooks; frontend/src/app/router.jsx; frontend/src/services/resources.js",
        "contracts": "stage-2-screen-action-inventory.md; actual versus planned API distinction in docs/api.md",
        "database": "No direct database access; depends on each module's authorized API",
        "evidence": "frontend/tests/unit; frontend/tests/e2e; required U01–U07 end-to-end business evidence pending",
        "status": "Shared UI exists; connected business workflow acceptance pending",
    },
    "architecture": {
        "screens": "Cross-cutting application layers and domain design",
        "code": "README.md; docs/architecture.md; docs/domain-model.md; docs/database-design.md; frontend/package-lock.json; backend/requirements-dev.lock; compose.yaml",
        "contracts": "docs/api.md; source-reconciliation.md (layout and contract differences)",
        "database": "Foundation migration implemented; later source-phase schemas planned incrementally",
        "evidence": "docs/traceability.md and docs/phases/phase-01-foundation.md cover Stage 1 only; full-domain evidence pending",
        "status": "Foundation/design baseline; entire-ERP invariants require future module evidence",
    },
    "operations": {
        "screens": "Health, operations/runbooks, reference workflow, regression and readiness",
        "code": "Makefile; scripts/test-local.sh; backend/tests; frontend/tests; docs/testing.md; docs/deployment.md; docs/backup-restore.md",
        "contracts": "erp-source/08_Phase_8_Testing_and_Optimization.md; source-reconciliation.md",
        "database": "Isolated PostgreSQL fixtures; full business dataset/attachment restore and upgrade evidence pending",
        "evidence": "Prior foundation checks are recorded in docs/testing.md; full F/M/I/T/A/P/R/U/O catalog and reference reconciliation not complete",
        "status": "Foundation evidence available; full ERP readiness unverified",
    },
}


def units(path):
    """Each bullet, table row, paragraph, or fenced example is a source unit.

    Headings are context and separators are formatting. Table headers are retained.
    Nothing else is
    discarded, including prerequisites, acceptance criteria and delivery gates.
    """
    rows = path.read_text().splitlines()
    headings, buffer, start, fenced = [], [], 0, False
    def flush():
        nonlocal buffer
        if not buffer:
            return None
        result = {"line": start, "section": " / ".join(headings), "text": "\n".join(buffer)}
        buffer = []
        return result
    for lineno, row in enumerate(rows, 1):
        if row.startswith("```"):
            if not fenced:
                if item := flush():
                    yield item
                start = lineno
            buffer.append(row)
            fenced = not fenced
            if not fenced and (item := flush()):
                yield item
            continue
        if fenced:
            buffer.append(row)
            continue
        if row.startswith("#"):
            if item := flush():
                yield item
            level = len(row) - len(row.lstrip("#"))
            headings = headings[:level-1] + [row.lstrip("# ")]
            continue
        if not row.strip() or row.strip() == "---" or re.fullmatch(r"[| :\-]+", row):
            if item := flush():
                yield item
            continue
        if re.match(r"^(- |\d+\. |\|)", row):
            if item := flush():
                yield item
            start, buffer = lineno, [row]
            if item := flush():
                yield item
            continue
        if not buffer:
            start = lineno
        buffer.append(row)
    if item := flush():
        yield item


def profile(filename, section):
    if filename == "00_Project_Standards.md":
        if "UI standards" in section:
            return "ui"
        if "Verification" in section:
            return "operations"
        return "architecture"
    if filename != "00_Original_Requirements.md":
        return {1:"foundation", 2:"master", 3:"inventory", 4:"trade", 5:"accounting", 6:"manufacturing", 7:"reports", 8:"operations"}[int(filename[:2])]
    for marker, workstream in [
        ("6. Reports", "reports"), ("7. User", "foundation"), ("8. UI/UX", "ui"),
        ("A. Dashboard", "reports"), ("B. Product", "master"), ("C. Inventory", "inventory"),
        ("D. Purchase", "trade"), ("E. Sales", "trade"), ("F. Customer", "master"),
        ("G. Supplier", "master"), ("H. Accounting", "accounting"), ("I. Manufacturing", "manufacturing"),
        ("J. Batch", "inventory"), ("K. Expense", "accounting"), ("L. Cash", "accounting"),
        ("M. Returns", "trade"), ("Phase 8", "operations"), ("Phase 7", "reports"),
        ("Phase 6", "manufacturing"), ("Phase 5", "accounting"), ("Phase 4", "trade"),
        ("Phase 3", "inventory"), ("Phase 2", "master"), ("Phase 1", "foundation"),
    ]:
        if marker in section:
            return workstream
    return "architecture"


def source_index(reports):
    report_ids = {r["source"]["line"]: r["id"] for r in reports}
    records = []
    for filename in REQUIRED:
        prefix = "ORIG" if filename.startswith("00_Original") else "STD" if filename.startswith("00_Project") else "P" + str(int(filename[:2]))
        for index, unit in enumerate(units(SOURCE / filename), 1):
            identifier = report_ids.get(unit["line"]) if prefix == "ORIG" else None
            unit.update(id=identifier or f"{prefix}-{index:03}", source="docs/erp-source/" + filename,
                        workstream=profile(filename, unit["section"]), status="mapped_not_acceptance_evidence")
            if (prefix == "ORIG" and "7. User Authentication" in unit["section"]) or (prefix == "P1" and any(name in unit["text"] for name in ("Business Owner", "Read-only User"))):
                unit["override"] = "OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer"
            records.append(unit)
    return {"schema_version": 1, "authority": "Ten populated sources plus user role override; source units are not a feature-completion count", "profiles": PROFILES, "requirements": records}


def render(index, reports, catalog):
    out = ["# ERP requirements traceability", "", "Updated against the complete source pack on 2026-11-24. This is a source coverage index, not an ERP completion certificate.", "",
           "The ten authoritative documents are listed in [source reconciliation](source-reconciliation.md). Original bytes and ZIP provenance are recorded in [manifest.json](erp-source/manifest.json). The confirmed role override `OVR-ROLES-01` takes precedence over older suggested roles. Empty legacy phase placeholders are not sources.", "",
           "Stable IDs identify every source paragraph, list item, table row and fenced example. Source units include context as well as requirements; their count must not be reported as an implementation percentage. The machine-readable [index](requirements-traceability.json) preserves full text, source lines and workstream mappings. Original report items use `R01.01`–`R01.40`, also used by the [report catalog](report-catalog.json).", "",
           "Mappings below identify implementation locations or planned owners. File existence, a route scaffold, and a permission reservation do not establish completed behavior. Prior Stage 1 evidence is explicitly distinguished from tests that have not run.", "",
           "## Workstream mapping", ""]
    for key, value in PROFILES.items():
        out += [f"### {key}", "", f"- Screens/actions: {value['screens']}.", f"- Code/service owner: {value['code']}.", f"- Contracts: {value['contracts']}.", f"- Database: {value['database']}.", f"- Verification: {value['evidence']}.", f"- Status: **{value['status']}**.", ""]
    out += ["## Source requirement index", "", "Each ID inherits its linked workstream's screens, code/service owner, database scope and evidence status. This broad source mapping does not replace the individual test evidence required before a completion claim. Compound source paragraphs still require multiple executable checks.", ""]
    for filename in REQUIRED:
        entries = [r for r in index["requirements"] if r["source"].endswith("/"+filename)]
        out += [f"### {filename}", "", f"{len(entries)} indexed source units. [Read the complete document](erp-source/{filename}).", "", "| ID | Source line and requirement/context | Workstream | Override |", "|---|---|---|---|"]
        for entry in entries:
            text = entry['text'].replace("\n", " ").replace("|", " / ").replace("`", "")
            if len(text) > 230:
                text = text[:227] + "…"
            out.append(f"| {entry['id']} | L{entry['line']}: {text} | [{entry['workstream']}](#{entry['workstream']}) | {entry.get('override', '—')} |")
        out.append("")
    out += ["## Report acceptance and unresolved work", "", "The exact report inventory is **8 inventory + 9 sales + 5 purchase + 11 accounting + 7 manufacturing = 40**. [Report verification](report-verification.md) defines separate totals, filters, permissions, drill-down, history and PDF/Excel cases for each report. None of those business checks has passed yet: report services and operational sources are not implemented.", "",
           "See [source reconciliation](source-reconciliation.md) for concrete path/layout differences and [screen/action inventory](stage-2-screen-action-inventory.md) for every current workspace's connection state. Full operational, accounting, manufacturing, worker and recovery acceptance remains pending. Missing source documents are no longer a blocker.", "",
           "Regenerate/check this index with `make traceability` / `make verify-sources`. These commands verify specification consistency only; they do not post transactions or verify report totals.", ""]
    inventory = ["# Stage 2 screen/action inventory", "", "Generated from the current workspace catalog. `connected` describes a transport connection, not proof that every action or workflow has been tested. `pending` is a proposed contract with no handler. `contract-gap` still lacks a resolved specific contract. Business actions remain visibly unavailable until implemented and verified.", "",
                 "Source authority: [complete requirements map](requirements-traceability.md). Cross-cutting routes: `/login` (public login), `/` (protected dashboard, metrics unavailable), `/system` (live health), `/roadmap` (planning), `/workspace/:group` (module navigation), forbidden/not-found/error states. Sidebar and route guards use current grants; backend authorization remains mandatory.", "",
                 "Shared behavior: `ResourcePage` renders lists/filter/pagination/error/unavailable states; `DetailPage` renders record tabs; `DraftPage` validates local inputs without persistence; `AdminEditorPage` connects user/role forms; `SettingsPage` connects currency/timezone changes. Report exports and business print actions have no persisted output yet. `WorkflowActions` lists review requirements only. IDs and decimal strings are preserved. See catalog.json for complete field schemas, line fields, tabs and columns, and workspaces/actions.js for action fields/grants/provisional states.", "",
                 "| Resource / route | Forms and actions | Read permission | API base (prefix /api/v1) | Connection |", "|---|---|---|---|---|"]
    for r in catalog:
        forms = "list/detail"
        if r["writable"]:
            forms += "; new/edit"
        if r["id"] == "business-settings":
            forms = "settings edit"
        actions = ", ".join(r["actions"]) or "none"
        if r["group"] == "Reports":
            actions += "; filter, drill-down, print, PDF/Excel (pending)"
        inventory.append(f"| {r['title']} `{r['path']}` | {forms}; {actions} | `{r['readPermission']}` | `{r.get('endpoint') or 'unresolved'}` | {r['status']} |")
    inventory += ["", "Create/edit use each resource's createPermission/updatePermission; action permissions combine resource.module with the action's grant in actions.js. Protected user/role controls add backend checks. Generic action states remain provisional until each domain service validates its exact state machine. Source-specific proposed APIs supersede conflicting early Stage 1 paths; see source-reconciliation.md. No nonexistent command is sent by the current transport.", ""]
    return {DOCS / "requirements-traceability.json": json.dumps(index, indent=2) + "\n",
            DOCS / "requirements-traceability.md": "\n".join(out),
            DOCS / "stage-2-screen-action-inventory.md": "\n".join(inventory)}


def check(archive=None):
    manifest = json.loads((SOURCE / "manifest.json").read_text())
    required = {f["path"].split("/")[-1] for f in manifest["files"] if f["authority"] == "required"}
    assert required == set(REQUIRED), "Required source set changed"
    for entry in manifest["files"]:
        raw = (ROOT / entry["path"]).read_bytes()
        assert len(raw) == entry["bytes"] and hashlib.sha256(raw).hexdigest() == entry["sha256"], entry["path"] + " has changed"
    if archive:
        archive = Path(archive)
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest["archive_sha256"], "ZIP checksum mismatch"
        with ZipFile(archive) as z:
            for entry in manifest["files"]:
                assert z.read(entry["archive_member"]) == (ROOT / entry["path"]).read_bytes(), entry["path"] + " differs from ZIP"
    assert manifest["overrides"][0]["roles"] == EXPECTED_ROLES
    actual_roles = runpy.run_path(str(ROOT / "backend/app/core/permissions.py"))["ROLE_GRANTS"]
    assert list(actual_roles) == EXPECTED_ROLES, "Backend role names/order differ from override"
    frontend_roles = re.findall(r"'([^']+)'", (ROOT / "frontend/src/auth/permissions.js").read_text())
    assert frontend_roles == EXPECTED_ROLES, "Frontend role names/order differ from override"
    assert all(p.endswith(":read") for p in actual_roles["Viewer"]), "Viewer must stay read-only"
    reports = json.loads((DOCS / "report-catalog.json").read_text())["reports"]
    catalog = json.loads((ROOT / "frontend/src/workspaces/catalog.json").read_text())
    report_screens = [r for r in catalog if r["group"] == "Reports"]
    screens = {r["sourceRequirement"]: r for r in report_screens}
    source_rows = (SOURCE / REQUIRED[0]).read_text().splitlines()
    section = source_rows[source_rows.index("# 6. Reports and Analytics"):source_rows.index("# 7. User Authentication and Permissions")]
    source_reports = [s[2:].rstrip(".") for s in section if s.startswith("- ")]
    assert [r["source_name"] for r in reports] == source_reports, "Source report names/order differ"
    assert Counter(r["family"] for r in reports) == {"Inventory":8,"Sales":9,"Purchases":5,"Accounting":11,"Manufacturing":7}
    assert len(report_screens) == len(screens) == len(reports) == 40
    assert len({r["path"] for r in report_screens}) == 40
    assert len({r["planned_api"] for r in reports}) == 40
    openapi = json.loads((DOCS / "openapi.json").read_text())["paths"]
    cases = json.loads((DOCS / "report-test-cases.json").read_text())["cases"]
    case_ids = {c["id"] for c in cases}
    assert len(cases) == len(case_ids) == 240, "Six distinct report cases required for each report"
    for number, r in enumerate(reports, 1):
        assert r["id"] == f"R01.{number:02}"
        assert source_rows[r["source"]["line"]-1] == "- " + r["source_name"] + "."
        screen = screens[r["id"]]
        assert screen["path"] == r["screen"] and screen["title"] == r["name"]
        assert "/api/v1" + screen["endpoint"] == r["planned_api"]
        assert screen["filters"] == r["filters"] and screen["columns"] == r["columns"]
        assert set(r["formats"]) == {"pdf", "xlsx"}
        assert set(r["test_cases"]) <= case_ids
        assert screen["readPermission"] == r["read_permission"] and screen["exportPermission"] == r["export_permission"]
        if r["api_status"] == "not_implemented":
            assert screen["status"] != "connected" and r["planned_api"] not in openapi, "Report status disagrees with OpenAPI"
        for c in (c for c in cases if c["requirement"] == r["id"]):
            assert c["status"] != "passed" or c.get("execution_evidence"), "Passed case lacks execution evidence"
    for path in ("/api/v1/reports/exports", "/api/v1/reports/exports/{id}", "/api/v1/reports/exports/{id}/download"):
        assert path not in openapi, "Export implementation added: update source reconciliation and report verification status"
    index = source_index(reports)
    ids = [r["id"] for r in index["requirements"]]
    assert len(ids) == len(set(ids)), "Duplicate source IDs"
    return index, reports, catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate source index and workspace inventory; never acceptance results")
    parser.add_argument("--archive", help="Also compare every source byte against the original ZIP")
    args = parser.parse_args()
    index, reports, catalog = check(args.archive)
    outputs = render(index, reports, catalog)
    for path, expected in outputs.items():
        if args.write:
            path.write_text(expected)
        else:
            assert path.exists() and path.read_text() == expected, str(path.relative_to(ROOT)) + " is stale; review then run make traceability"
    print(f"Source consistency PASS: 10 required documents, {len(index['requirements'])} source units, 40 reports (8/9/5/11/7), 240 planned report cases, exact 9 roles.")
    print("This check does not verify business totals, exports, permissions or ERP completion.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        print(f"Source consistency FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
