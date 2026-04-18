# Autonomous Tool Capability Matrix

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Tool Capability Matrix |
| Status | Docs-only autonomous toolchain integration draft |
| Snapshot | S5-AUTONOMOUS-TOOLCHAIN-INTEGRATION-2026-04-18-001 |
| Stage | s5-autonomous-toolchain-integration |
| Baseline commit | `3e106c324b37f22114fdb8243c6ef158d471408f` |

This matrix records current governed tool capability understanding. It does not authorize execution, credentials, browser automation, external review completion, staging, commit, push, full gate, or release packaging by itself.

## 2. Capability Matrix

| Tool | Interface | Detected? | Verified command/path | Current maturity | Allowed autonomous actions | Prohibited actions | Required approval | Failure/HOLD conditions | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Codex app automation | Current chat/workspace automation | Yes | Current Codex session | L1 | Plan, draft allowed docs, edit allowed files, run safe local checks, prepare review prompts. | Red-3, launch, production deployment, external pilot execution, credentials, real data, public endpoint work, S5-B/S5-D reopen, ORDIV work, staging/commit/push without explicit authorization. | Current stage prompt and active policy; Red-1/Red-2 require exact `DELEGATED_APPROVER_GO` where policy requires it. | Charter unreadable, expired delegation, unclear lane, unexpected files, unresolved HOLD. | Product memory remains repo-governed docs and manifest, not chat context. |
| Codex CLI | Local CLI | Yes | `codex.exe` visible by safe command detection | L1 | Candidate future helper after command behavior is governed. | Self-authorizing Red work, credential handling, unsupervised external access, staging/commit/push without explicit authority. | Separate governed command/use decision before autonomous execution reliance. | CLI missing, non-zero, ambiguous output, writes outside scope. | Detected only; not used in this stage. |
| VS Code CLI | Local workspace CLI | Yes | `code.cmd` visible by safe command detection | L1 | Workspace file surface and possible local editing helper when governed. | Treating workspace as product memory, installing dependencies, launching external flows, staging/commit/push without explicit authority. | Current stage prompt for docs edits; human confirmation for day-1 staging/commit/push. | CLI missing, ambiguous workspace, file scope mismatch. | VS Code is execution surface only. |
| Claude Code via `cc switch` API tool | API tool bridge | Human-confirmed path; not locally executed by Codex in this stage | User reports `claude.exe` is unusable; Claude Code access is through the `cc switch` API tool | L1 | Generate review prompt; possible future review-only API runner after non-interactive behavior is verified. | Edits, staging, commit, push, code execution claims, external pilot execution, credential handling. | Separate verification of non-interactive review-only API command/request behavior before automated use. | `cc switch` unavailable, API error/non-zero, ambiguous output, attempts to edit, unclear review status. | Until verified, automation must HOLD for human/tool execution; `claude.exe` must not be used as the Claude Code path. |
| Claude Web in AdsPower browser/profile | AdsPower browser/external review path | User-confirmed manual surface; automation not verified | Manual AdsPower browser tab only; Local API reachable but requires API key | L0 | Prepare external review prompt for manual transfer into AdsPower/Claude Web. | Automated login, AdsPower profile/session control, credential/session access, cookies/tokens/auth headers, claiming external review PASS without governed result. | Human/manual external review or later governed AdsPower browser path with non-secret API-key provisioning. | AdsPower unavailable, API key unavailable, profile/session unknown, credential prompt, network ambiguity. | Required for high-risk triggers already defined in governance docs; screenshot/user report confirms location only, not automation authority. |
| AdsPower browser/profile control | Browser/profile launcher candidate | User-confirmed as Claude Web container; local process and API endpoint detected; automation not verified | Local API returns `Require api-key`; no key used in this stage | L0 | None beyond documenting candidate status. | AdsPower/browser launch, profile automation, login, cookie/session inspection, credential handling, printing API keys. | Separate governed AdsPower browser verification route and human-controlled API-key secret path. | Launcher missing, API key missing, profile/session unknown, credential prompt, automation ambiguity. | No AdsPower/browser control is claimed. |
| Browser 2 candidate | Browser launcher candidate | Not verified | Not verified in this stage | L0 | None beyond documenting candidate status. | Browser launch, browser automation, login, cookie/session inspection, credential handling. | Separate governed browser verification route. | Launcher missing, session unknown, credential prompt, automation ambiguity. | No browser control is claimed. |
| Git/GitHub remote | Local Git and configured upstream | Yes | `git status`, `git rev-parse HEAD`, and upstream equality checked | L1 | Inspect status, diff, branch, and upstream state; prepare staging plan. | Day-1 staging/commit/push without explicit human confirmation; force-push; rewriting history; including unrelated files. | Explicit human confirmation for day-1 staging/commit/push; later lane-specific authority. | Dirty unexpected files, upstream mismatch, network ambiguity, push ambiguity. | Existing untracked files remain out of scope. |
| Release/gate scripts | Repo scripts | Yes | `scripts\git_preflight.py` tracked in repo | L1 | Reference gate commands and prepare closeout plan. | Full gate or release packaging unless explicitly authorized after review. | Current stage prompt or later closeout instruction. | Gate failure, script missing, generated artifact ambiguity, release verification mismatch. | This stage does not run full gate. |

## 3. Current Maturity Summary

Current claimed maturity is L1: local CLI detection for Codex/VS Code/Codex CLI, user-confirmed Claude Code access through `cc switch`, and manual review prompt transfer. L2, L3, L4, and L5 are not claimed by this stage.

No credentials, tokens, cookies, auth headers, session data, or account material may be entered into repo, chat, prompts, review packs, or logs.
