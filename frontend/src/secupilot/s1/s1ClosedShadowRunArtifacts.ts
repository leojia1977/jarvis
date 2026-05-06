export interface S1ArtifactManifestEntry {
  fileName: string;
  path: string;
  sha256: string;
  retentionClass: string;
  retainAllowed: boolean;
  containsRawPayload: boolean;
  containsSecretOrToken: boolean;
  containsCustomerVisibleArtifact: boolean;
}

export interface S1CaseSummaryEntry {
  caseId: string;
  title: string;
  sourceId: string;
  decisionHint: string;
  reviewerAction: string;
}

export type S1LocalReviewDecision =
  | "PASS_TO_NEXT_LOCAL_RC"
  | "PASS_WITH_NOTES_TO_NEXT_LOCAL_RC"
  | "HOLD_FOR_FIXES"
  | "NO_GO_FOR_CURRENT_PRODUCT_PATH";

export const S1_CLOSED_SHADOW_RUN_ARTIFACTS = {
  schemaVersion: "secupilot.s1.frontend_fixture.v1",
  runId: "S1-CLOSED-SHADOW-2026-04-30-001",
  goRecordRef: "SECUPILOT-S1-CLOSED-SHADOW-GO-20260430-001",
  provider: "fixture",
  inputRef: "mock_data/s0_synthetic/qwen_fact_bundle",
  inputKind: "qwen_fact_bundle_directory",
  dataMode: "SYNTHETIC_PACKAGE_ONLY",
  startTimeUtc: "2026-04-30T11:37:45Z",
  endTimeUtc: "2026-04-30T11:37:45Z",
  finalOutcome: "S1_CLOSED_SHADOW_PASS_WITH_NOTES",
  exitCode: 10,
  passHoldReason:
    "Closed-shadow fixture metadata capture completed; reviewer signoff required.",
  reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED",
  nextStep: "FRONTEND_ARTIFACT_VIEW",
  caseCount: 20,
  qwenUsed: false,
  canShowInLocalDemo: true,
  canDeployToCustomerProduction: false,
  safetyScan: {
    findingCount: 0,
    holdCount: 0,
    noGoCount: 0,
    scannedFields: 1201,
    scannedStringValues: 740,
    objectCount: 20
  },
  boundaries: {
    customerVisibleOutput: false,
    productionWriteback: false,
    productionConnectors: false,
    qwenAutonomousAction: false,
    rawPayloadRetention: false,
    secretRetention: false
  },
  localReview: {
    schemaVersion: "secupilot.s1.local_review_record.v1",
    candidate: "LOCAL_OFFLINE_TRIAL_RC_004",
    sourceCandidate: "LOCAL_OFFLINE_TRIAL_RC_003",
    reviewer: "LOCAL_REVIEWER",
    defaultDecision: "PASS_WITH_NOTES_TO_NEXT_LOCAL_RC" satisfies S1LocalReviewDecision,
    allowedDecisions: [
      "PASS_TO_NEXT_LOCAL_RC",
      "PASS_WITH_NOTES_TO_NEXT_LOCAL_RC",
      "HOLD_FOR_FIXES",
      "NO_GO_FOR_CURRENT_PRODUCT_PATH"
    ] satisfies S1LocalReviewDecision[],
    defaultNotes:
      "RC-003 passed; RC-004 adds a self-contained local/offline reviewer handoff view.",
    handoff: {
      reviewMode: "LOCAL_OFFLINE_REVIEW_ONLY",
      packagePath: "artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-004",
      readmePath:
        "artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-004/REVIEWER_README.md",
      zipName: "s1-closed-shadow-local-offline-trial-rc-004-review-package-20260506.zip",
      requiredChecks: [
        "REVIEWER_README.md",
        "package_manifest.json",
        "final_status.json",
        "case_summary.json",
        "artifact_manifest.json",
        "safety_scan.json",
        "playwright/s1-run-desktop.png",
        "playwright/s1-run-mobile.png"
      ],
      boundaryChecks: [
        "real_data=false",
        "masked_real_data=false",
        "live_qwen_api=false",
        "live_connectors=false",
        "production_writeback=false",
        "customer_visible_output=false"
      ]
    }
  },
  artifacts: [
    {
      fileName: "run_record.json",
      path: "artifacts/s1_closed_shadow_runs/2026-04-30-001/run_record.json",
      sha256: "a229362348df05ef6acaa70a22837e7c967084bb505f26c177f93970e3161b57",
      retentionClass: "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
      retainAllowed: true,
      containsRawPayload: false,
      containsSecretOrToken: false,
      containsCustomerVisibleArtifact: false
    },
    {
      fileName: "safety_scan.json",
      path: "artifacts/s1_closed_shadow_runs/2026-04-30-001/safety_scan.json",
      sha256: "1feb98bc48a6a9e681f06a2cd3e325e5d3d8d2ba0e7dbd773ea7284f1973cf15",
      retentionClass: "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
      retainAllowed: true,
      containsRawPayload: false,
      containsSecretOrToken: false,
      containsCustomerVisibleArtifact: false
    },
    {
      fileName: "case_summary.json",
      path: "artifacts/s1_closed_shadow_runs/2026-04-30-001/case_summary.json",
      sha256: "58a2fddfbada698e9215ad61e652bd240d28ed21a9acd1f7fa5525a8e2a9c6af",
      retentionClass: "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
      retainAllowed: true,
      containsRawPayload: false,
      containsSecretOrToken: false,
      containsCustomerVisibleArtifact: false
    },
    {
      fileName: "final_status.json",
      path: "artifacts/s1_closed_shadow_runs/2026-04-30-001/final_status.json",
      sha256: "45f57750a303b42596ef30eb013b96d30b65759725741c1fa5e8b18d43692690",
      retentionClass: "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
      retainAllowed: true,
      containsRawPayload: false,
      containsSecretOrToken: false,
      containsCustomerVisibleArtifact: false
    },
    {
      fileName: "RUN_RECORD.md",
      path: "artifacts/s1_closed_shadow_runs/2026-04-30-001/RUN_RECORD.md",
      sha256: "b0c58bcf49626265a89af379145676dcee01d17b1c85035a204e0c2a05b04bd5",
      retentionClass: "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
      retainAllowed: true,
      containsRawPayload: false,
      containsSecretOrToken: false,
      containsCustomerVisibleArtifact: false
    }
  ] satisfies S1ArtifactManifestEntry[],
  cases: [
    {
      caseId: "UAT-01",
      title: "NTLM lateral movement with AR escalation",
      sourceId: "s0-cv-uat-01-ntlm-lateral",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-02",
      title: "Observation window expiry and manual re-approval",
      sourceId: "s0-cv-uat-02-observation-expiry",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-03",
      title: "Terminal Lock after approval",
      sourceId: "s0-cv-uat-03-terminal-lock",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-04",
      title: "Ransomware staging with mass file operations",
      sourceId: "s0-cv-uat-04-ransomware-staging",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-05",
      title: "Kerberoasting / SPN burst pattern",
      sourceId: "s0-cv-uat-05-kerberoasting-spn",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-06",
      title: "MFA fatigue + impossible travel",
      sourceId: "s0-cv-uat-06-mfa-fatigue",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-07",
      title: "OAuth consent abuse / suspicious app grant",
      sourceId: "s0-cv-uat-07-oauth-consent",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-08",
      title: "Cloud key leak / abnormal API access",
      sourceId: "s0-cv-uat-08-cloud-key",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-09",
      title: "DNS tunneling / long-domain beaconing",
      sourceId: "s0-cv-uat-09-dns-tunneling",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-10",
      title: "C2 beaconing with low-and-slow intervals",
      sourceId: "s0-cv-uat-10-c2-low-slow",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-11",
      title: "Living-off-the-land WMI / PsExec movement",
      sourceId: "s0-cv-uat-11-lotl-wmi-psexec",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-12",
      title: "Privileged VPN login from unusual geography",
      sourceId: "s0-cv-uat-12-vpn-geo",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-13",
      title: "Insider bulk download without malware",
      sourceId: "s0-cv-uat-13-insider-download",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-14",
      title: "CMDB business tags unavailable",
      sourceId: "s0-cv-uat-14-cmdb-unavailable",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-15",
      title: "Audit trail empty",
      sourceId: "s0-cv-uat-15-audit-empty",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-16",
      title: "Audit trail source unavailable",
      sourceId: "s0-cv-uat-16-audit-unavailable",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-17",
      title: "Search history recorded > current downgrade",
      sourceId: "s0-cv-uat-17-history-downgrade",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-18",
      title: "Search history current > recorded upgrade prohibited",
      sourceId: "s0-cv-uat-18-history-upgrade-prohibited",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-19",
      title: "P3 manager summary without host raw evidence",
      sourceId: "s0-cv-uat-19-p3-summary-no-raw",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    },
    {
      caseId: "UAT-20",
      title: "Prompt injection attempt inside analyst comment",
      sourceId: "s0-cv-uat-20-prompt-injection",
      decisionHint: "REVIEW_REQUIRED",
      reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED"
    }
  ] satisfies S1CaseSummaryEntry[]
} as const;
