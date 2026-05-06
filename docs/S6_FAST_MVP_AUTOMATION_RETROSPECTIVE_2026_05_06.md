# S6 Fast MVP Automation Retrospective 2026-05-06

## Summary

The five-day automation produced useful implementation work but lost efficiency at `MVP-09`.

Completed:

```text
MVP-05 S1 artifact viewer Playwright smoke
MVP-06 S1 artifact validator
MVP-07 external-output provider path
MVP-08 local demo package builder
```

Stopped at:

```text
MVP-09 Claude review capture
HOLD_MVP_09_REVIEW_SCOPE_MISMATCH
```

## What Worked

The queue did not idle at the start. It selected one item at a time, implemented code/tests/artifacts, ran verification, and committed passing work.

The stop condition also did its safety job: a review output referenced files outside the current queue item scope, so the automation did not continue blindly into MVP-10.

## What Failed

The queue treated every HOLD as a permanent blocking condition and then retried the same MVP-09 failure on later scheduled runs.

That behavior was safe but inefficient:

```text
same blocking item
same external review tool
same scope mismatch class
no deterministic recovery path
no automatic item status transition
no resume marker for later items
```

## New Rule

Automation should distinguish:

```text
blocking safety HOLD
recoverable tool/evidence HOLD
non-blocking review-quality HOLD
queue-exhausted stop
```

Safety HOLDs still stop the queue:

```text
real data / masked-real data detected
secret/token/auth/raw payload detected
customer-visible output detected
production write-back detected
live connector or live Qwen/API attempted
unexpected dirty files outside item scope
```

Review-quality HOLDs should use a bounded recovery path:

```text
retry once with stricter subject-file list
if still out-of-scope, preserve evidence
reject out-of-scope findings
accept in-scope findings as follow-up or remediate immediately
write a closeout decision
resume the next queue item only after tests and fast gate pass
```

## MVP-09 Specific Fix

For `MVP-09`, the correct recovery is:

```text
do not rerun broad Claude review indefinitely
preserve raw review files
scope-filter findings
reject broad backend findings for the Fast MVP queue
remediate accepted MVP-08 package-builder findings
mark MVP-09 closed after remediation
resume at MVP-10
```

## Prompt Change Required

The cron prompt should say:

```text
If MVP-09 closeout records MVP_09_CLOSED_WITH_SCOPE_FILTERED_FINDINGS_REMEDIATED, do not rerun MVP-09. Resume at MVP-10.

If a review command produces out-of-scope findings twice, stop retrying that command. Preserve evidence, write a scope-filtered HOLD closeout, and request or apply a bounded remediation only for in-scope findings.
```

## Operating Principle

Automation is useful when it can make bounded progress without pretending every uncertainty is fatal.

The target behavior is:

```text
stop for safety
recover for tooling noise
commit verified increments
never invent scope
never loop on the same known failure
```
