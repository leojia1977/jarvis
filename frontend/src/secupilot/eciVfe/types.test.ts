import eciCorrelationSchema from "../../../../schemas/eci_vfe_correlation.schema.json";
import eciAssessmentSchema from "../../../../schemas/eci_chain_assessment.schema.json";
import vfeForecastSchema from "../../../../schemas/vfe_forecast_candidate.schema.json";
import eci001 from "../../../../mock_data/eci_vfe/eci_cases/eci_case_001_early_stage_recon.json";
import eci002 from "../../../../mock_data/eci_vfe/eci_cases/eci_case_002_initial_access_to_persistence.json";
import eci003 from "../../../../mock_data/eci_vfe/eci_cases/eci_case_003_lateral_movement_suspected.json";
import eci004 from "../../../../mock_data/eci_vfe/eci_cases/eci_case_004_prompt_injection_process_name.json";
import eci005 from "../../../../mock_data/eci_vfe/eci_cases/eci_case_005_prompt_injection_user_agent.json";
import eci006 from "../../../../mock_data/eci_vfe/eci_cases/eci_case_006_prompt_injection_code_comment.json";
import vfe001 from "../../../../mock_data/eci_vfe/vfe_cases/vfe_case_001_config_risk_candidate.json";
import vfe002 from "../../../../mock_data/eci_vfe/vfe_cases/vfe_case_002_privilege_boundary_candidate.json";
import vfe003 from "../../../../mock_data/eci_vfe/vfe_cases/vfe_case_003_false_positive_candidate.json";
import vfe004 from "../../../../mock_data/eci_vfe/vfe_cases/vfe_case_004_malicious_banner_injection.json";
import vfe005 from "../../../../mock_data/eci_vfe/vfe_cases/vfe_case_005_malicious_config_comment_injection.json";
import {
  ECI_VFE_SCHEMA_VERSION,
  EciCaseFixture,
  VfeCaseFixture,
  isMetadataOnlyFixture,
  isNonAuthoritativeLlmField
} from "./types";

const eciFixtures = [eci001, eci002, eci003, eci004, eci005, eci006] as EciCaseFixture[];
const vfeFixtures = [vfe001, vfe002, vfe003, vfe004, vfe005] as VfeCaseFixture[];

const forbiddenFixtureText = [
  /raw_log/i,
  /raw_payload/i,
  /host_raw_evidence/i,
  /authorization/i,
  /bearer/i,
  /api[_-]?key/i,
  /access[_-]?token/i,
  /private[_-]?key/i,
  /credential/i,
  /exploit step/i,
  /\bPoC\b/i,
  /\bpayload\b/i,
  /action_command/i,
  /automatic containment/i
];

describe("ECI/VFE v0.2 fixture model", () => {
  it("keeps every fixture synthetic, metadata-only, and local/offline", () => {
    for (const fixture of [...eciFixtures, ...vfeFixtures]) {
      expect(fixture.schema_version).toBe(ECI_VFE_SCHEMA_VERSION);
      expect(isMetadataOnlyFixture(fixture)).toBe(true);
      expect(fixture.no_action_boundary).toMatchObject({
        human_review_required: true,
        automatic_containment_allowed: false,
        production_writeback_allowed: false
      });
    }
  });

  it("covers the mandatory ECI and VFE fixture set", () => {
    expect(eciFixtures.map((fixture) => fixture.fixture_id)).toEqual([
      "eci_case_001_early_stage_recon",
      "eci_case_002_initial_access_to_persistence",
      "eci_case_003_lateral_movement_suspected",
      "eci_case_004_prompt_injection_process_name",
      "eci_case_005_prompt_injection_user_agent",
      "eci_case_006_prompt_injection_code_comment"
    ]);
    expect(vfeFixtures.map((fixture) => fixture.fixture_id)).toEqual([
      "vfe_case_001_config_risk_candidate",
      "vfe_case_002_privilege_boundary_candidate",
      "vfe_case_003_false_positive_candidate",
      "vfe_case_004_malicious_banner_injection",
      "vfe_case_005_malicious_config_comment_injection"
    ]);
  });

  it("models prompt-injection fixtures as sanitized metadata without retaining raw instructions", () => {
    const injectionFixtures = [...eciFixtures, ...vfeFixtures].filter(
      (fixture) => fixture.prompt_injection_handling.input_injection_detected
    );

    expect(injectionFixtures.map((fixture) => fixture.fixture_id)).toEqual([
      "eci_case_004_prompt_injection_process_name",
      "eci_case_005_prompt_injection_user_agent",
      "eci_case_006_prompt_injection_code_comment",
      "vfe_case_004_malicious_banner_injection",
      "vfe_case_005_malicious_config_comment_injection"
    ]);

    for (const fixture of injectionFixtures) {
      expect(fixture.prompt_injection_handling.raw_injection_retained).toBe(false);
      expect(fixture.prompt_injection_handling.forbidden_output_present).toBe(false);
      expect(fixture.prompt_injection_handling.sanitized_summary).toContain(
        "untrusted field contained instruction-like text"
      );
    }
  });

  it("keeps forbidden fixture content out of metadata-only files", () => {
    for (const fixture of [...eciFixtures, ...vfeFixtures]) {
      const text = JSON.stringify(fixture);
      for (const pattern of forbiddenFixtureText) {
        expect(text).not.toMatch(pattern);
      }
      expect(Object.prototype.hasOwnProperty.call(fixture, "attack_path")).toBe(false);
    }
  });

  it("requires evidence gaps to include urgency and collection-window guidance", () => {
    for (const fixture of [...eciFixtures, ...vfeFixtures]) {
      expect(fixture.expected_evidence_gaps.length).toBeGreaterThan(0);
      for (const gap of fixture.expected_evidence_gaps) {
        expect(gap.allowed_scope).toBe("metadata_only");
        expect(["CRITICAL", "HIGH", "MEDIUM", "LOW"]).toContain(gap.urgency);
        expect(gap.window_closes_in).toMatch(/^\d+(m|h)$/);
        expect(gap.deadline_basis.length).toBeGreaterThan(0);
        expect(gap.fallback_if_missed.length).toBeGreaterThan(0);
      }
    }
  });

  it("keeps VFE query controls audit-required and non-bulk", () => {
    for (const fixture of vfeFixtures) {
      expect(fixture.query_context.audit_required).toBe(true);
      expect(fixture.query_context.bulk_export).toBe(false);
      expect(fixture.query_context.asset_scope).not.toBe("bulk");
      expect(fixture.query_context.requester_alias).toMatch(/^SecuPilot-/);
      expect(fixture.attack_path_defensive_summary).toBeTruthy();
    }
  });

  it("keeps LLM-derived fields non-authoritative by default", () => {
    expect(
      isNonAuthoritativeLlmField({
        value: "supporting signal only",
        source: "LLM_INFERENCE",
        confidence: 0.65,
        evidence_refs: ["fixture:eci-vfe"],
        is_authoritative: false
      })
    ).toBe(true);
  });

  it("declares schema fields required by the baseline", () => {
    const schemaText = JSON.stringify([eciAssessmentSchema, vfeForecastSchema, eciCorrelationSchema]);

    for (const required of [
      "source_type",
      "trust_level",
      "is_authoritative",
      "evidence_refs",
      "query_context",
      "attack_path_defensive_summary",
      "case_upgrade_allowed"
    ]) {
      expect(schemaText).toContain(required);
    }
  });
});
