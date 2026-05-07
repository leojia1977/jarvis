export type S1QwenProviderMode =
  | "fixture"
  | "external-output"
  | "qwen-cloud-disabled";

export interface S1QwenProviderModeContract {
  mode: S1QwenProviderMode;
  label: string;
  status: "available" | "disabled";
  liveCallAllowed: boolean;
  secretsAllowed: boolean;
  connectorAllowed: boolean;
  description: string;
}

export const S1_QWEN_PROVIDER_CONTRACT = {
  schemaVersion: "secupilot.s1.qwen_provider_contract.v1",
  activeMode: "qwen-cloud-disabled" satisfies S1QwenProviderMode,
  liveCallAllowed: false,
  secretMaterialAllowed: false,
  connectorCallAllowed: false,
  customerVisibleOutputAllowed: false,
  productionWritebackAllowed: false,
  configRef: "contracts/s1_qwen_provider_contract_v0_1.json",
  modes: [
    {
      mode: "fixture",
      label: "Fixture provider（本地 fixture）",
      status: "available",
      liveCallAllowed: false,
      secretsAllowed: false,
      connectorAllowed: false,
      description: "使用 repo 内已打包的 synthetic metadata，不发起 live 调用。"
    },
    {
      mode: "external-output",
      label: "External output provider（外部输出导入）",
      status: "available",
      liveCallAllowed: false,
      secretsAllowed: false,
      connectorAllowed: false,
      description: "只从本地文件导入已批准的 metadata-only 模型输出。"
    },
    {
      mode: "qwen-cloud-disabled",
      label: "Qwen cloud provider（未启用）",
      status: "disabled",
      liveCallAllowed: false,
      secretsAllowed: false,
      connectorAllowed: false,
      description: "仅为规划骨架；live Qwen 必须另行明确授权后才能启用。"
    }
  ] satisfies S1QwenProviderModeContract[]
} as const;
