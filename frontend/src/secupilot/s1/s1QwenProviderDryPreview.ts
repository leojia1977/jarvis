export const S1_QWEN_PROVIDER_DRY_PREVIEW = {
  schemaVersion: "secupilot.s1.qwen_provider_dry_preview.v1",
  providerMode: "dry_contract_only",
  dataMode: "SYNTHETIC_ONLY",
  inputPackageRef: "mock_data/qwen_provider_contract/valid_response.json",
  fixtureSourceRef: "mock_data/s0_synthetic/qwen_fact_bundle",
  caseCount: 1,
  outputPreview: {
    caseId: "UAT-01",
    riskLevel: "medium",
    reviewerAction: "REVIEW_AND_SIGNOFF_REQUIRED",
    confidence: 0.74,
    modelSummary:
      "Synthetic metadata indicates a lateral movement pattern that requires human review.",
    limitationNote:
      "Synthetic metadata-only contract; no raw customer evidence, write-back, or autonomous action."
  },
  allowedMetadataFields: [
    "case_id",
    "title",
    "risk_level",
    "evidence_metadata_refs",
    "model_summary",
    "reviewer_action",
    "confidence",
    "limitation_note"
  ],
  rejectedFieldLabels: [
    "原始载荷字段",
    "密钥或令牌字段",
    "认证头字段",
    "生产连接器输出",
    "写回动作字段",
    "自主审批/驳回/关闭字段"
  ],
  boundaries: {
    qwenUsed: false,
    liveQwenApi: false,
    liveConnectors: false,
    customerVisibleOutput: false,
    productionWriteback: false,
    autonomousQwenAction: false,
    secretMaterialAllowed: false
  }
} as const;
