# AGENTS.md

## Default Mode: Code-Only

All agents and automations working in this repository must use Code-Only mode by default.

Do:

- Implement product code, integration code, tests, fixtures, schemas, and configuration needed to make the product work.
- Run only relevant tests and validation commands after changes.
- Keep changes narrow, reviewable, and tied to the current product task.
- Preserve enterprise-grade safety through code, tests, guards, validation, and permission boundaries.

Do not create or update documentation by default.

Forbidden unless the owner explicitly asks for the exact file or deliverable:

- README updates.
- Architecture decision records.
- API documentation.
- Interface specifications.
- Process documents.
- Collaboration workflows.
- Team updates.
- Status reports.
- Closeout reports.
- Changelogs.
- Roadmaps.
- Review packages.
- Generated summaries.
- Diagram or flowchart files.
- Standalone test report files.

## Comments

Use code comments and docstrings only when they clarify non-obvious implementation logic.

Do not use inline comments as a substitute for reports, process notes, roadmap notes, or team communication.

## Multi-Agent Work

For multi-agent or automation work:

- Implement only the necessary code, tests, fixtures, schemas, and configuration.
- Do not generate collaboration-process files, handoff documents, workflow diagrams, or coordination reports.
- Communicate brief status in the conversation or automation message only, not by writing repository report files.

## Safety

Maintain high safety and enterprise standards without producing extra documentation.

Hard boundaries:

- Do not connect real systems unless explicitly authorized.
- Do not use customer-side data, credentials, connector source material, secrets, or tokens.
- Do not publish, deploy, or create externally accessible environments unless explicitly authorized.
- Do not perform autonomous security actions or online state changes.
- Do not stage, commit, push, reset, checkout, or clean unless explicitly authorized.

## Exceptions

Allowed without additional approval:

- This `AGENTS.md` file.
- Source code.
- Tests.
- Test fixtures.
- Schemas.
- Build or runtime configuration.
- Minimal code comments or docstrings where needed.

Any other non-code artifact requires explicit owner approval naming the file or deliverable.

## Uncertainty Rule

If an agent is unsure whether a change is allowed under Code-Only mode, it must ask the owner before creating or modifying files.
