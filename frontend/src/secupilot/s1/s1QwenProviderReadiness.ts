export const S1_QWEN_PROVIDER_READINESS = {
  schemaVersion: "secupilot.s1.qwen_provider_readiness.v1",
  status: "QWEN_SYNTHETIC_PROVIDER_STUB_READY_NO_NETWORK",
  productLabel: "本地合成建议已就绪",
  productDescription:
    "已经可以把本地合成安全案例转换为 metadata-only 模型建议，用于产品预览和后续接入演练；不联网、不读取运行时密钥值。",
  providerStubMode: "本地合成建议预览（不联网）",
  caseCount: 20,
  runId: "QWEN-LIVE-SYNTHETIC-2026-05-08-001",
  providerOutputRef:
    "artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json",
  providerReportRef:
    "artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json",
  runtimeConfigReportRef:
    "artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json",
  nextStep:
    "下一步只能做本地配置核验和产品预览；真实调用仍需要单独 synthetic-only live GO。",
  boundaries: {
    qwenUsed: false,
    liveQwenApi: false,
    networkCall: false,
    secretValuesRead: false,
    secretValuesRetained: false,
    liveConnectors: false,
    customerVisibleOutput: false,
    productionWriteback: false,
    autonomousQwenAction: false
  }
} as const;
