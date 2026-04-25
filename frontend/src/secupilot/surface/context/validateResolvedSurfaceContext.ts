import {
  ActionMode,
  ActionPermission,
  ARStatus,
  CaseState,
  CoverageLevel,
  ResolvedSurfaceContext,
  Role,
  SecurityHaltCode,
  Surface,
  SwitchState,
  ValidationResult
} from "./types";

const TOP_LEVEL_FIELDS = new Set([
  "fixture_meta",
  "session",
  "surface",
  "case",
  "action_request",
  "action_permissions",
  "resolved_visibility",
  "honesty",
  "audit_trail",
  "ui_messages"
]);

const AUTHORITY_SOURCE_FIELDS = new Set([
  "url",
  "url_params",
  "urlParams",
  "query",
  "query_params",
  "localStorage",
  "sessionStorage",
  "storage",
  "window_location"
]);

const ROLES = new Set<Role>(["P0", "P1", "P2", "P3"]);
const COVERAGE_LEVELS = new Set<CoverageLevel>(["L0", "L1", "L2", "L3"]);
const SURFACES = new Set<Surface>([
  "P1_CASE_DETAIL",
  "P2_APPROVAL",
  "P3_MANAGER",
  "CROSS_SURFACE"
]);
const CASE_STATES = new Set<CaseState>([
  "UNDER_INVESTIGATION",
  "PENDING_APPROVAL",
  "OBSERVATION_WINDOW",
  "APPROVED_PENDING_EXECUTION",
  "CLOSED"
]);
const AR_STATUSES = new Set<ARStatus>([
  "PENDING_APPROVAL",
  "APPROVED_PENDING_EXECUTION",
  "OBSERVATION_WINDOW",
  "REJECTED",
  "WITHDRAWN",
  "CANCELLED"
]);
const ACTION_MODES = new Set<Exclude<ActionMode, null>>([
  "IMMEDIATE",
  "DELAYED",
  "OBSERVE_ONLY"
]);
const SWITCH_STATES = new Set<SwitchState>(["ON", "DEGRADED", "OFF", "READONLY"]);
const ACTION_PERMISSIONS = new Set<ActionPermission>([
  "ALLOW",
  "CONFIRM",
  "ESCALATE",
  "DENY",
  "READONLY",
  "DISABLED",
  "HIDDEN"
]);

const SURFACE_ROLE_ALLOWLIST: Record<Exclude<Surface, "CROSS_SURFACE">, Role> = {
  P1_CASE_DETAIL: "P1",
  P2_APPROVAL: "P2",
  P3_MANAGER: "P3"
};

const COVERAGE_RANK: Record<CoverageLevel, number> = {
  L0: 0,
  L1: 1,
  L2: 2,
  L3: 3
};

const P3_PRIVILEGED_KEYS = [
  "raw_evidence",
  "rawEvidence",
  "host_raw_evidence",
  "hostRawEvidence",
  "raw_event_payload",
  "rawEventPayload",
  "raw_event",
  "rawEvent",
  "process_tree",
  "processTree",
  "technical_dom_payload",
  "technicalDomPayload",
  "internal_tool",
  "internalTool",
  "node_detail",
  "nodeDetail",
  "t_node_detail",
  "contains_host_level_raw_evidence"
];

function halt(code: SecurityHaltCode, reason: string): ValidationResult {
  return { ok: false, code, reason };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

function hasOwn(value: Record<string, unknown>, key: string) {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function validateStringRecordValues<T extends string>(
  value: unknown,
  allowed: Set<T>,
  code: SecurityHaltCode,
  label: string
): ValidationResult | undefined {
  if (!isRecord(value)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", `${label} must be an object`);
  }

  for (const [key, item] of Object.entries(value)) {
    if (typeof item !== "string" || !allowed.has(item as T)) {
      return halt(code, `${label}.${key} has unsupported value`);
    }
  }

  return undefined;
}

function validateUiMessages(value: unknown): ValidationResult | undefined {
  if (!isRecord(value)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "ui_messages must be an object");
  }

  for (const [key, item] of Object.entries(value)) {
    const valid =
      item === null ||
      typeof item === "string" ||
      (Array.isArray(item) && item.every((message) => typeof message === "string"));
    if (!valid) {
      return halt("SH-08_INVALID_CONTEXT_SHAPE", `ui_messages.${key} has invalid shape`);
    }
  }

  return undefined;
}

function validateHonesty(value: unknown): ValidationResult | undefined {
  if (!isRecord(value)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "honesty must be an object");
  }

  for (const key of [
    "what_would_raise_confidence",
    "what_would_disprove_current_verdict",
    "unsupported_claims"
  ]) {
    if (!isStringArray(value[key])) {
      return halt("SH-08_INVALID_CONTEXT_SHAPE", `honesty.${key} must be a string array`);
    }
  }

  return undefined;
}

function containsForbiddenP3Payload(value: unknown): boolean {
  if (Array.isArray(value)) {
    return value.some((item) => containsForbiddenP3Payload(item));
  }

  if (!isRecord(value)) {
    return false;
  }

  for (const [key, item] of Object.entries(value)) {
    if (P3_PRIVILEGED_KEYS.includes(key)) {
      if (key === "contains_host_level_raw_evidence") {
        return item === true;
      }
      if (item === "OFF" || item === false || item === null) {
        continue;
      }
      return true;
    }

    if (containsForbiddenP3Payload(item)) {
      return true;
    }
  }

  return false;
}

function isAllowedDocumentationIp(value: string): boolean {
  return (
    /^192\.0\.2\.\d{1,3}$/.test(value) ||
    /^198\.51\.100\.\d{1,3}$/.test(value) ||
    /^203\.0\.113\.\d{1,3}$/.test(value)
  );
}

function containsDisallowedRealDataMarker(value: unknown): boolean {
  if (typeof value === "string") {
    const emailMatches = value.match(/\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b/gi) ?? [];
    if (
      emailMatches.some((email) => {
        const domain = email.split("@")[1]?.toLowerCase() ?? "";
        return domain !== "corp.example" && domain !== "example.com" && !domain.endsWith(".corp.example");
      })
    ) {
      return true;
    }

    const ipMatches = value.match(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g) ?? [];
    if (ipMatches.some((ip) => !isAllowedDocumentationIp(ip))) {
      return true;
    }

    const domainMatches =
      value.match(/\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|co|ai|dev|cn)\b/gi) ?? [];
    return domainMatches.some((domain) => {
      const normalized = domain.toLowerCase();
      return (
        normalized !== "example.com" &&
        normalized !== "corp.example" &&
        !normalized.endsWith(".corp.example")
      );
    });
  }

  if (Array.isArray(value)) {
    return value.some((item) => containsDisallowedRealDataMarker(item));
  }

  if (isRecord(value)) {
    return Object.values(value).some((item) => containsDisallowedRealDataMarker(item));
  }

  return false;
}

function hasCoverageCeilingViolation(context: Record<string, unknown>): boolean {
  const caseValue = context.case;
  const visibility = context.resolved_visibility;
  if (!isRecord(caseValue) || !isRecord(visibility)) {
    return false;
  }

  const caseCoverage = caseValue.coverage_level as CoverageLevel;
  const effectiveVisibility = visibility.effective_visibility_level as CoverageLevel;
  if (COVERAGE_LEVELS.has(caseCoverage) && COVERAGE_LEVELS.has(effectiveVisibility)) {
    if (COVERAGE_RANK[effectiveVisibility] > COVERAGE_RANK[caseCoverage]) {
      return true;
    }
  }

  return Boolean(
    visibility.coverage_ceiling_override ||
      visibility.coverageCeilingOverride ||
      visibility.promotes_off_fields ||
      visibility.promote_off_fields
  );
}

function hasP2OnlyPermissionForNonP2(context: Record<string, unknown>): boolean {
  const session = context.session;
  if (!isRecord(session) || session.role === "P2") {
    return false;
  }

  const permissions = context.action_permissions;
  if (!isRecord(permissions)) {
    return false;
  }

  return Object.entries(permissions).some(([key, value]) => {
    const p2OnlyKey = /approve|reject|delay|observe|execute|execution|action_mode|strong_confirm|decision/i.test(
      key
    );
    return p2OnlyKey && ["ALLOW", "CONFIRM", "ESCALATE"].includes(String(value));
  });
}

function hasNonP2ActionMode(context: Record<string, unknown>): boolean {
  const session = context.session;
  const actionRequest = context.action_request;
  if (!isRecord(session) || session.role === "P2" || !isRecord(actionRequest)) {
    return false;
  }

  return actionRequest.action_mode !== null && actionRequest.action_mode !== undefined;
}

export function validateResolvedSurfaceContext(input: unknown): ValidationResult {
  if (!isRecord(input)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "context root must be an object");
  }

  for (const key of Object.keys(input)) {
    if (AUTHORITY_SOURCE_FIELDS.has(key)) {
      return halt("SH-08_UNAUTHORIZED_CONTEXT_SOURCE", `${key} cannot be a context authority`);
    }
    if (!TOP_LEVEL_FIELDS.has(key)) {
      return halt("SH-08_UNEXPECTED_TOP_LEVEL_FIELD", `${key} is not allowed at context root`);
    }
  }

  for (const key of [
    "fixture_meta",
    "session",
    "surface",
    "case",
    "action_permissions",
    "resolved_visibility",
    "honesty",
    "audit_trail",
    "ui_messages"
  ]) {
    if (!hasOwn(input, key)) {
      return halt("SH-08_INVALID_CONTEXT_SHAPE", `${key} is required`);
    }
  }

  const fixtureMeta = input.fixture_meta;
  if (!isRecord(fixtureMeta)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "fixture_meta must be an object");
  }
  if (fixtureMeta.source !== "fully_artificial") {
    return halt("SH-08_NON_ARTIFICIAL_FIXTURE", "fixture_meta.source must be fully_artificial");
  }
  if (fixtureMeta.real_data_derived !== false) {
    return halt("SH-08_REAL_DATA_DERIVED", "fixture_meta.real_data_derived must be false");
  }
  if (fixtureMeta.contains_real_customer_data !== false) {
    return halt(
      "SH-08_REAL_DATA_DERIVED",
      "fixture_meta.contains_real_customer_data must be false"
    );
  }
  if (fixtureMeta.allowed_for !== "mock-only bounded frontend implementation") {
    return halt("SH-08_NON_ARTIFICIAL_FIXTURE", "fixture_meta.allowed_for is not authorized");
  }

  const session = input.session;
  if (!isRecord(session) || typeof session.role !== "string" || !ROLES.has(session.role as Role)) {
    return halt("SH-08_UNSUPPORTED_ENUM", "session.role is unsupported");
  }

  if (typeof input.surface !== "string" || !SURFACES.has(input.surface as Surface)) {
    return halt("SH-08_UNSUPPORTED_ENUM", "surface is unsupported");
  }

  const surface = input.surface as Surface;
  const role = session.role as Role;
  if (surface !== "CROSS_SURFACE" && SURFACE_ROLE_ALLOWLIST[surface] !== role) {
    return halt("SH-08_SURFACE_ROLE_MISMATCH", `${surface} is not allowed for ${role}`);
  }

  const caseValue = input.case;
  if (!isRecord(caseValue)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "case must be an object");
  }
  if (typeof caseValue.case_id !== "string" || caseValue.case_id.trim() === "") {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "case.case_id is required");
  }
  if (
    typeof caseValue.case_state !== "string" ||
    !CASE_STATES.has(caseValue.case_state as CaseState)
  ) {
    return halt("SH-08_UNSUPPORTED_ENUM", "case.case_state is unsupported");
  }
  if (
    typeof caseValue.coverage_level !== "string" ||
    !COVERAGE_LEVELS.has(caseValue.coverage_level as CoverageLevel)
  ) {
    return halt("SH-08_UNSUPPORTED_ENUM", "case.coverage_level is unsupported");
  }
  if (typeof caseValue.expert_mode_active !== "boolean") {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "case.expert_mode_active must be boolean");
  }

  if (hasOwn(input, "action_request")) {
    const actionRequest = input.action_request;
    if (!isRecord(actionRequest)) {
      return halt("SH-08_INVALID_CONTEXT_SHAPE", "action_request must be an object when present");
    }
    if (typeof actionRequest.ar_id !== "string" || actionRequest.ar_id.trim() === "") {
      return halt("SH-08_INVALID_CONTEXT_SHAPE", "action_request.ar_id is required");
    }
    if (
      typeof actionRequest.ar_status !== "string" ||
      !AR_STATUSES.has(actionRequest.ar_status as ARStatus)
    ) {
      return halt("SH-08_UNSUPPORTED_ENUM", "action_request.ar_status is unsupported");
    }
    if (
      actionRequest.action_mode !== null &&
      (typeof actionRequest.action_mode !== "string" ||
        !ACTION_MODES.has(actionRequest.action_mode as Exclude<ActionMode, null>))
    ) {
      return halt("SH-08_UNSUPPORTED_ENUM", "action_request.action_mode is unsupported");
    }
    if (typeof actionRequest.version !== "string" || actionRequest.version.trim() === "") {
      return halt("SH-08_INVALID_CONTEXT_SHAPE", "action_request.version is required");
    }
  }

  const permissionsResult = validateStringRecordValues(
    input.action_permissions,
    ACTION_PERMISSIONS,
    "SH-08_UNSUPPORTED_ENUM",
    "action_permissions"
  );
  if (permissionsResult) {
    return permissionsResult;
  }

  const visibility = input.resolved_visibility;
  if (!isRecord(visibility)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "resolved_visibility must be an object");
  }
  if (
    typeof visibility.effective_visibility_level !== "string" ||
    !COVERAGE_LEVELS.has(visibility.effective_visibility_level as CoverageLevel)
  ) {
    return halt(
      "SH-08_UNSUPPORTED_ENUM",
      "resolved_visibility.effective_visibility_level is unsupported"
    );
  }

  const pagesResult = validateStringRecordValues(
    visibility.pages,
    SWITCH_STATES,
    "SH-08_UNSUPPORTED_ENUM",
    "resolved_visibility.pages"
  );
  if (pagesResult) {
    return pagesResult;
  }

  const fieldsResult = validateStringRecordValues(
    visibility.fields,
    SWITCH_STATES,
    "SH-08_UNSUPPORTED_ENUM",
    "resolved_visibility.fields"
  );
  if (fieldsResult) {
    return fieldsResult;
  }

  if (hasOwn(visibility, "allowed_actions")) {
    const allowedActionsResult = validateStringRecordValues(
      visibility.allowed_actions,
      ACTION_PERMISSIONS,
      "SH-08_UNSUPPORTED_ENUM",
      "resolved_visibility.allowed_actions"
    );
    if (allowedActionsResult) {
      return allowedActionsResult;
    }
  }

  const honestyResult = validateHonesty(input.honesty);
  if (honestyResult) {
    return honestyResult;
  }

  if (!Array.isArray(input.audit_trail) || !input.audit_trail.every(isRecord)) {
    return halt("SH-08_INVALID_CONTEXT_SHAPE", "audit_trail must be an array of objects");
  }

  const uiMessagesResult = validateUiMessages(input.ui_messages);
  if (uiMessagesResult) {
    return uiMessagesResult;
  }

  if (hasCoverageCeilingViolation(input)) {
    return halt("SH-08_COVERAGE_CEILING_VIOLATION", "resolved visibility exceeds coverage ceiling");
  }

  if (hasP2OnlyPermissionForNonP2(input) || hasNonP2ActionMode(input)) {
    return halt("SH-08_CONFUSION_ATTACK_PAYLOAD", "non-P2 context carries P2-only decision authority");
  }

  if (containsForbiddenP3Payload(input)) {
    return halt(
      "SH-08_P3_PRIVILEGED_PAYLOAD_PRESENT",
      "context includes raw technical payload"
    );
  }

  if (containsDisallowedRealDataMarker(input)) {
    return halt("SH-08_REAL_DATA_DERIVED", "context contains disallowed real-data-like markers");
  }

  return { ok: true, context: input as ResolvedSurfaceContext };
}
