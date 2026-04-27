import type { ResolvedSurfaceContext, SwitchState } from "../context/types";
import { adaptCoreSurfaceFixturePhase } from "./coreSurfaceFixtureAdapter";
import type { FixtureKind, FixtureRegistryEntry } from "./fixtureTypes";

type UiMessages = ResolvedSurfaceContext["ui_messages"];
type VisibilityFields = ResolvedSurfaceContext["resolved_visibility"]["fields"];

function cloneFixture<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function phaseContext(phase: number): ResolvedSurfaceContext {
  return cloneFixture(adaptCoreSurfaceFixturePhase(phase));
}

function withUiMessages(
  context: ResolvedSurfaceContext,
  uiMessages: UiMessages
): ResolvedSurfaceContext {
  return {
    ...context,
    ui_messages: {
      ...context.ui_messages,
      ...uiMessages
    }
  };
}

function withFields(
  context: ResolvedSurfaceContext,
  fields: Record<string, SwitchState>
): ResolvedSurfaceContext {
  return {
    ...context,
    resolved_visibility: {
      ...context.resolved_visibility,
      fields: {
        ...context.resolved_visibility.fields,
        ...fields
      }
    }
  };
}

function withCoverage(
  context: ResolvedSurfaceContext,
  coverageLevel: ResolvedSurfaceContext["case"]["coverage_level"],
  effectiveVisibilityLevel: ResolvedSurfaceContext["resolved_visibility"]["effective_visibility_level"],
  fields: Record<string, SwitchState>
): ResolvedSurfaceContext {
  return {
    ...withFields(context, fields),
    case: {
      ...context.case,
      coverage_level: coverageLevel
    },
    resolved_visibility: {
      ...context.resolved_visibility,
      effective_visibility_level: effectiveVisibilityLevel,
      fields: {
        ...context.resolved_visibility.fields,
        ...fields
      }
    }
  };
}

function phase07CrossSurfaceContext(): ResolvedSurfaceContext {
  const context = phaseContext(5);
  return withUiMessages(
    {
      ...context,
      surface: "CROSS_SURFACE",
      resolved_visibility: {
        ...context.resolved_visibility,
        pages: {
          case_detail: "READONLY",
          approval_surface: "READONLY",
          manager_view: "READONLY",
          cross_surface_walkthrough: "ON"
        }
      }
    },
    {
      phase_name: "Phase 07 - cross-surface validated walkthrough",
      cross_surface_scope: "fixture-only route handoff rehearsal",
      mock_only_notice:
        "CROSS_SURFACE is a test harness fixture only and carries no production routing authority."
    }
  );
}

function boundaryP3AuditUnavailable(): ResolvedSurfaceContext {
  return withUiMessages(
    withFields(phaseContext(6), {
      approval_audit_summary: "DEGRADED",
      host_raw_evidence: "OFF"
    }),
    {
      missing_signal_notice: "P3 audit summary unavailable in mock fixture.",
      missing_signal_notice_source: 'data-message-source="ui_messages"',
      expected_ui: ["manager summary remains read-only", "raw host evidence remains hidden"]
    }
  );
}

function boundaryP2CmdbTagsUnavailable(): ResolvedSurfaceContext {
  return withUiMessages(
    withFields(phaseContext(2), {
      cmdb_business_tags: "DEGRADED",
      blast_radius: "OFF"
    }),
    {
      missing_signal_notice: "CMDB tags unavailable in mock fixture.",
      missing_signal_notice_source: 'data-message-source="ui_messages"',
      expected_ui: ["inline missing signal notice", "approval controls do not gain extra authority"]
    }
  );
}

function boundaryDirtyUpdateDuringObservationWindow(): ResolvedSurfaceContext {
  return withUiMessages(
    withFields(phaseContext(3), {
      observation_window: "READONLY",
      dirty_update_state: "DEGRADED"
    }),
    {
      inline_warning: "Fixture dirty update detected during observation window.",
      observation_window_state: "active-readonly",
      expected_ui: ["status remains OBSERVATION_WINDOW", "old operation state remains disabled"]
    }
  );
}

function boundaryConcurrencyStaleApproveRejected(): ResolvedSurfaceContext {
  const context = phaseContext(3);
  return withUiMessages(
    {
      ...context,
      action_permissions: {
        ...context.action_permissions,
        approve_action: "DISABLED",
        reject_action: "DISABLED",
        observe_only_action: "READONLY",
        delay_action: "DISABLED"
      }
    },
    {
      inline_warning: "Stale approve was rejected by fixture concurrency state.",
      concurrency_state: "stale-approve-rejected",
      expected_ui: ["inline warning required", "toast cannot replace inline warning"]
    }
  );
}

function resolverL1BlastRadiusPayload(): ResolvedSurfaceContext {
  return withUiMessages(
    withCoverage(phaseContext(0), "L1", "L1", {
      contextual_evidence_summary: "DEGRADED",
      blast_radius: "OFF",
      blast_radius_payload: "OFF",
      lateral_topology: "OFF"
    }),
    {
      resolver_degradation: "coverage L1 keeps blast_radius OFF instead of triggering SH-08",
      expected_ui: ["blast radius hidden under L1", "context remains valid"]
    }
  );
}

function resolverL1LineageConfidenceDegraded(): ResolvedSurfaceContext {
  return withUiMessages(
    withCoverage(phaseContext(0), "L1", "L1", {
      contextual_evidence_summary: "DEGRADED",
      lineage_confidence: "DEGRADED",
      confidence_raise_reasons: "READONLY"
    }),
    {
      resolver_degradation: "lineage confidence is degraded under L1 without unlocking hidden fields",
      expected_ui: ["lineage confidence degraded", "no coverage ceiling override"]
    }
  );
}

function resolverP3TechnicalDetailRedaction(): ResolvedSurfaceContext {
  return withUiMessages(
    withFields(phaseContext(6), {
      technical_detail: "OFF",
      host_raw_evidence: "OFF",
      process_tree: "OFF"
    }),
    {
      resolver_degradation: "P3 technical detail is redacted for manager summary fixture.",
      expected_ui: ["manager audit summary only", "no DOM-level raw evidence"]
    }
  );
}

function resolverSearchHistoryCurrentLowerThanRecorded(): ResolvedSurfaceContext {
  return withUiMessages(
    withCoverage(phaseContext(0), "L2", "L1", {
      contextual_evidence_summary: "DEGRADED",
      search_history_current: "DEGRADED",
      search_history_recorded: "READONLY"
    }),
    {
      resolver_degradation: "current visibility lower than recorded visibility remains bounded",
      expected_ui: ["current level message shown", "recorded level does not become authority"]
    }
  );
}

function resolverSearchHistoryCurrentHigherThanRecorded(): ResolvedSurfaceContext {
  return withUiMessages(
    withCoverage(phaseContext(0), "L3", "L2", {
      contextual_evidence_summary: "ON",
      search_history_current: "READONLY",
      search_history_recorded: "DEGRADED",
      coverage_l3_fields: "OFF"
    }),
    {
      resolver_degradation: "current visibility higher than recorded visibility does not unlock L3 fields",
      expected_ui: ["L3-only fields stay OFF", "effective visibility remains L2"]
    }
  );
}

function asInvalidContext(context: ResolvedSurfaceContext): Record<string, unknown> {
  return cloneFixture(context) as unknown as Record<string, unknown>;
}

function poisonMissingSurface(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  delete context.surface;
  return context;
}

function poisonUnsupportedSurface(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  context.surface = "P2_APPROVAL_SURFACE";
  return context;
}

function poisonSurfaceRoleMismatch(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  context.surface = "P3_MANAGER";
  return context;
}

function poisonP1ActionModeImmediate(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(1));
  const actionRequest = context.action_request as Record<string, unknown>;
  actionRequest.action_mode = "IMMEDIATE";
  return context;
}

function poisonP1P2OnlyPermission(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  const permissions = context.action_permissions as Record<string, unknown>;
  permissions.approve_action = "ALLOW";
  return context;
}

function poisonP3HostRawEvidencePayload(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(6));
  const auditTrail = context.audit_trail as Record<string, unknown>[];
  auditTrail.push({
    audit_id: "AUD-POISON-HOST-RAW",
    event: "HOST_RAW_EVIDENCE_ATTEMPTED",
    host_raw_evidence: {
      process_tree: ["synthetic-not-renderable.exe"]
    }
  });
  return context;
}

function poisonFixtureMetaRealDataDerived(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  const fixtureMeta = context.fixture_meta as Record<string, unknown>;
  fixtureMeta.real_data_derived = true;
  return context;
}

function poisonInvalidCaseState(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  const caseValue = context.case as Record<string, unknown>;
  caseValue.case_state = "ESCALATED";
  return context;
}

function poisonInvalidArStatus(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(2));
  const actionRequest = context.action_request as Record<string, unknown>;
  actionRequest.ar_status = "APPROVED";
  return context;
}

function poisonMissingFixtureMeta(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  delete context.fixture_meta;
  return context;
}

function poisonTopLevelAuthorityField(): Record<string, unknown> {
  const context = asInvalidContext(phaseContext(0));
  context.url_params = { role: "P2", coverage: "L3" };
  return context;
}

function entry(
  id: string,
  kind: FixtureKind,
  description: string,
  context: ResolvedSurfaceContext | Record<string, unknown>,
  expectedValidation: FixtureRegistryEntry["expectedValidation"] = "pass"
): FixtureRegistryEntry {
  return {
    id,
    kind,
    description,
    expectedValidation,
    context
  };
}

const PHASE_ENTRIES: FixtureRegistryEntry[] = [
  entry("phase-00-p1-under-investigation", "phase", "P1 under-investigation case detail", phaseContext(0)),
  entry("phase-01-p1-submitted-waiting-on-p2", "phase", "P1 submitted AR awaiting P2", phaseContext(1)),
  entry("phase-02-p2-pending-approval", "phase", "P2 pending approval with no action mode", phaseContext(2)),
  entry("phase-03-p2-observation-window-active", "phase", "P2 observe-only active window", phaseContext(3)),
  entry("phase-04-p2-observation-expired-returned-pending", "phase", "P2 observation expired and returned to pending", phaseContext(4)),
  entry("phase-05-p2-approved-pending-execution", "phase", "P2 approved pending execution", phaseContext(5)),
  entry("phase-06-p3-manager-audit-summary", "phase", "P3 manager summary without raw host evidence", phaseContext(6)),
  entry("phase-07-cross-surface-full-walkthrough", "phase", "CROSS_SURFACE fixture-only walkthrough", phase07CrossSurfaceContext())
];

const BOUNDARY_CASE_ENTRIES: FixtureRegistryEntry[] = [
  entry("boundary-p3-audit-summary-unavailable", "boundary_case", "P3 audit summary missing-signal degradation", boundaryP3AuditUnavailable()),
  entry("boundary-p2-cmdb-tags-unavailable", "boundary_case", "P2 CMDB tags missing-signal degradation", boundaryP2CmdbTagsUnavailable()),
  entry("boundary-dirty-update-during-observation-window", "boundary_case", "Dirty update represented during observe-only window", boundaryDirtyUpdateDuringObservationWindow()),
  entry("boundary-concurrency-stale-approve-rejected", "boundary_case", "Stale approve rejection with inline warning state", boundaryConcurrencyStaleApproveRejected())
];

const RESOLVER_DEGRADATION_ENTRIES: FixtureRegistryEntry[] = [
  entry("resolver-l1-blast-radius-payload", "resolver_degradation", "L1 blast radius payload resolves to OFF without SH-08", resolverL1BlastRadiusPayload()),
  entry("resolver-l1-lineage-confidence-degraded", "resolver_degradation", "L1 lineage confidence degrades without widening coverage", resolverL1LineageConfidenceDegraded()),
  entry("resolver-p3-technical-detail-redaction", "resolver_degradation", "P3 technical details remain OFF", resolverP3TechnicalDetailRedaction()),
  entry("resolver-search-history-current-lower-than-recorded", "resolver_degradation", "Current level below recorded level remains bounded", resolverSearchHistoryCurrentLowerThanRecorded()),
  entry("resolver-search-history-current-higher-than-recorded", "resolver_degradation", "Current level above recorded level does not unlock L3", resolverSearchHistoryCurrentHigherThanRecorded())
];

const POISON_PILL_ENTRIES: FixtureRegistryEntry[] = [
  entry("poison-missing-surface", "poison_pill", "Missing required surface", poisonMissingSurface(), "fail_closed"),
  entry("poison-unsupported-surface", "poison_pill", "Unsupported source surface name", poisonUnsupportedSurface(), "fail_closed"),
  entry("poison-surface-role-mismatch", "poison_pill", "P1 role carrying P3 manager surface", poisonSurfaceRoleMismatch(), "fail_closed"),
  entry("poison-p1-action-mode-immediate", "poison_pill", "P1 attempts to choose IMMEDIATE", poisonP1ActionModeImmediate(), "fail_closed"),
  entry("poison-p1-p2-only-action-permission", "poison_pill", "P1 carries P2-only approval authority", poisonP1P2OnlyPermission(), "fail_closed"),
  entry("poison-p3-host-raw-evidence-payload", "poison_pill", "P3 fixture attempts to carry raw host evidence", poisonP3HostRawEvidencePayload(), "fail_closed"),
  entry("poison-fixture-meta-real-data-derived", "poison_pill", "Fixture metadata claims real data derivation", poisonFixtureMetaRealDataDerived(), "fail_closed"),
  entry("poison-invalid-enum-case-state", "poison_pill", "Unsupported case_state enum", poisonInvalidCaseState(), "fail_closed"),
  entry("poison-invalid-enum-ar-status", "poison_pill", "Unsupported ar_status enum", poisonInvalidArStatus(), "fail_closed"),
  entry("poison-missing-fixture-meta", "poison_pill", "Missing fixture_meta", poisonMissingFixtureMeta(), "fail_closed"),
  entry("poison-unknown-top-level-authority-field", "poison_pill", "Top-level URL params authority attempt", poisonTopLevelAuthorityField(), "fail_closed")
];

export const FIXTURE_REGISTRY_ENTRIES: readonly FixtureRegistryEntry[] = [
  ...PHASE_ENTRIES,
  ...BOUNDARY_CASE_ENTRIES,
  ...RESOLVER_DEGRADATION_ENTRIES,
  ...POISON_PILL_ENTRIES
];

export const FIXTURE_REGISTRY = new Map(
  FIXTURE_REGISTRY_ENTRIES.map((registryEntry) => [registryEntry.id, registryEntry])
);

export function getFixtureRegistryEntry(id: string): FixtureRegistryEntry {
  const registryEntry = FIXTURE_REGISTRY.get(id);
  if (!registryEntry) {
    throw new Error(`Unknown mock fixture id: ${id}`);
  }
  return registryEntry;
}

export function listFixtureIds(kind?: FixtureKind): string[] {
  return FIXTURE_REGISTRY_ENTRIES.filter((registryEntry) => !kind || registryEntry.kind === kind).map(
    (registryEntry) => registryEntry.id
  );
}

export function cloneFixtureContext(value: unknown): unknown {
  return cloneFixture(value);
}

export function boundaryCaseFields(id: string): VisibilityFields {
  const entryValue = getFixtureRegistryEntry(id).context;
  const context = entryValue as ResolvedSurfaceContext;
  return cloneFixture(context.resolved_visibility.fields);
}
