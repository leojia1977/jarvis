# S6 Fast MVP MVP-09 Claude Review Capture Closeout (2026-05-01)

## Scope

- Queue item: `MVP-09`
- Allowed evidence scope:
  - `artifacts/reviews/claude_code/*`
  - this closeout file
- Review target after scope filtering:
  - `scripts/package_s1_local_demo.py`
  - `backend/tests/test_package_s1_local_demo.py`
  - `artifacts/local_demo_packages/s1-closed-shadow-2026-04-30-001/package_manifest.json`

## Command

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
claude --print "Review only the current git diff for the SecuPilot Fast MVP queue item. Check correctness, unsafe data handling, secret/token/raw payload retention, production write-back, customer-visible output, tests, and overengineering. Do not edit files. Return findings ordered by severity, or say no findings."
```

## Raw Evidence Files

```text
artifacts/reviews/claude_code/mvp-09-current-diff-review-20260501T122936Z.txt
artifacts/reviews/claude_code/mvp-09-current-diff-review-20260501T123004Z.txt
artifacts/reviews/claude_code/mvp-09-current-diff-review-20260501T162752Z.txt
```

## Scope Filter

The original automation correctly stopped on:

```text
HOLD_MVP_09_REVIEW_SCOPE_MISMATCH
```

Accepted as MVP-08 package-builder findings:

```text
absolute local paths in package_manifest.json
RUN_RECORD.md copied without text safety scan
runtime assert used as guard
missing test for artifact_manifest forbidden flags
missing invalid JSON / CLI tests
source/copy SHA-256 verification gap
```

Rejected as out-of-scope for this Fast MVP queue item:

```text
main.py exception response findings
runtime_service.py path response findings
edr_adapter.py / siem_adapter.py gap_reason findings
persistent_case.py nested mutability finding
config.py version disclosure finding
```

Those rejected findings may be reviewed later as a separate backend hardening stream, but they do not block MVP-09 closeout or the MVP-10~MVP-13 Fast MVP queue.

## Corrective Patch

The accepted findings were remediated in the MVP-09 closeout patch:

```text
package manifest now uses portable paths
package copies verify source SHA-256 equals destination SHA-256
Markdown/text artifacts are scanned for credential-like forbidden text patterns
runtime assert was replaced with an explicit HOLD check
tests now cover manifest forbidden flags, markdown pattern detection, invalid JSON, portable paths, and CLI run()
local demo package manifest was regenerated without local absolute paths
```

## Decision

```text
MVP_09_CLOSED_WITH_SCOPE_FILTERED_FINDINGS_REMEDIATED
QUEUE_CAN_RESUME_AT_MVP_10
```

No real data, masked-real data, live Qwen/API/connectors, production write-back, customer-visible deploy/publish/output, secrets, tokens, auth headers, or raw payloads were introduced by this closeout.
