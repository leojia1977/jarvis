import { useMemo, useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  ClipboardCheck,
  FileText,
  Lock,
  MessageSquareText,
  MonitorCheck,
  PlayCircle,
  ShieldCheck
} from "lucide-react";
import { S1_CLOSED_SHADOW_RUN_ARTIFACTS } from "./s1ClosedShadowRunArtifacts";
import { S1_QWEN_PROVIDER_CONTRACT } from "./s1QwenProviderContract";

type FeedbackDecision =
  | "READY_FOR_NEXT_INTERNAL_TRIAL"
  | "NEEDS_SMALL_FIX"
  | "HOLD_LOCAL_TRIAL";

const FEEDBACK_OPTIONS: Array<{
  decision: FeedbackDecision;
  label: string;
  description: string;
}> = [
  {
    decision: "READY_FOR_NEXT_INTERNAL_TRIAL",
    label: "可继续内部试用",
    description: "页面和材料足够清楚，可进入下一轮内部试用。"
  },
  {
    decision: "NEEDS_SMALL_FIX",
    label: "需要小修",
    description: "可以继续，但需要先修正文案、路径、截图或说明。"
  },
  {
    decision: "HOLD_LOCAL_TRIAL",
    label: "暂缓本地试用",
    description: "当前包对评审者仍不够清楚，先暂停继续传播。"
  }
];

function yesNo(value: boolean): string {
  return value ? "是" : "否";
}

export function S1LocalTrialView() {
  const run = S1_CLOSED_SHADOW_RUN_ARTIFACTS;
  const trial = run.localTrial;
  const qwenContract = S1_QWEN_PROVIDER_CONTRACT;
  const [feedbackDecision, setFeedbackDecision] = useState<FeedbackDecision>(
    "READY_FOR_NEXT_INTERNAL_TRIAL"
  );
  const [feedbackNotes, setFeedbackNotes] = useState(
    "评审者可以从 README、manifest、final_status、安全扫描和截图完成本地离线检查。"
  );
  const launchCommand = `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ${trial.launcherScript}`;
  const trialActions = [
    {
      title: "打开本地试用",
      description: "进入本地浏览器页面，先确认候选版本和试用边界。",
      value: trial.localUrl
    },
    {
      title: "核验评审材料",
      description: "按中文入口、manifest、运行状态、安全扫描和截图完成离线检查。",
      value: trial.deliveryPackagePath
    },
    {
      title: "记录本地反馈",
      description: "在页面中预览反馈结论，再写入评审模板或 governed review note。",
      value: "本地反馈预览"
    }
  ];
  const materialStatus = [
    ["中文入口", "已就绪"],
    ["检查清单", "已就绪"],
    ["反馈模板", "已就绪"],
    ["截图与证据", "已打包"]
  ] as const;
  const boundaryFacts = [
    ["真实数据", false],
    ["脱敏真实数据", false],
    ["Live Qwen/API", false],
    ["Live connectors", false],
    ["生产写回", run.boundaries.productionWriteback],
    ["客户可见输出", run.boundaries.customerVisibleOutput],
    ["Push", false]
  ] as const;
  const feedbackPreview = useMemo(
    () => ({
      schema_version: "secupilot.s1.local_trial_feedback_preview.v1",
      candidate: trial.candidate,
      decision: feedbackDecision,
      notes: feedbackNotes,
      record_scope: "LOCAL_BROWSER_PREVIEW_ONLY",
      artifact_write: false,
      backend_write: false,
      qwen_api_call: false,
      connector_call: false,
      customer_visible_output: false,
      production_writeback: false
    }),
    [feedbackDecision, feedbackNotes, trial.candidate]
  );

  return (
    <section
      aria-labelledby="s1-trial-title"
      className="page-region s1-trial-view"
      data-customer-visible-output="false"
      data-live-connectors="false"
      data-live-qwen-api="false"
      data-production-writeback="false"
      data-push="false"
      data-real-data="false"
      data-testid="s1-local-trial-view"
    >
      <header className="s1-trial-header">
        <div>
          <p className="summary-kicker">本地离线试用</p>
          <h1 id="s1-trial-title">SecuPilot 本地离线试用中心</h1>
          <p className="s1-trial-lede">
            从这里启动一次内部本地试用、核验评审材料并记录反馈。当前页面只用于
            synthetic package 的离线检查，不连接真实系统。
          </p>
          <dl className="s1-trial-header-facts">
            <div>
              <dt>候选版本</dt>
              <dd data-testid="s1-trial-candidate">{trial.candidate}</dd>
            </div>
            <div>
              <dt>就绪状态</dt>
              <dd data-testid="s1-trial-readiness">{trial.readiness}</dd>
            </div>
            <div>
              <dt>Run ID</dt>
              <dd>{run.runId}</dd>
            </div>
          </dl>
        </div>
        <span className="s1-trial-status">
          <ShieldCheck aria-hidden="true" size={18} />
          仅限内部本地/离线
        </span>
      </header>

      <section aria-label="本地试用入口" className="s1-product-entry-grid">
        {trialActions.map((action, index) => (
          <article key={action.title}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <div>
              <strong>{action.title}</strong>
              <p>{action.description}</p>
              <code>{action.value}</code>
            </div>
            <ArrowRight aria-hidden="true" size={18} />
          </article>
        ))}
      </section>

      <section aria-label="本地离线试用概览" className="s1-trial-kpi-grid">
        <article>
          <span>案例数</span>
          <strong>{run.caseCount}</strong>
          <p>{run.inputRef}</p>
        </article>
        <article>
          <span>安全扫描命中</span>
          <strong>{run.safetyScan.findingCount}</strong>
          <p>{`${run.safetyScan.scannedStringValues} 个字符串已扫描`}</p>
        </article>
        <article>
          <span>Qwen 调用</span>
          <strong>{yesNo(run.qwenUsed)}</strong>
          <p>仅 fixture 路径</p>
        </article>
        <article>
          <span>客户上线授权</span>
          <strong>{yesNo(run.canDeployToCustomerProduction)}</strong>
          <p>未授权客户可见输出</p>
        </article>
      </section>

      <section className="s1-trial-product-grid">
        <article
          className="s1-artifact-panel s1-trial-primary-panel"
          data-testid="s1-trial-launcher-panel"
        >
          <div className="s1-panel-title">
            <PlayCircle aria-hidden="true" size={18} />
            <h2>开始试用</h2>
          </div>
          <p>
            当前候选包已通过本地离线边界检查。先打开试用入口，再按材料状态完成核验。
          </p>
          <div className="s1-trial-primary-action">
            <span>本地入口</span>
            <strong>{trial.localUrl}</strong>
          </div>
          <div className="s1-launch-command" aria-label="本地试用启动命令">
            <MonitorCheck aria-hidden="true" size={18} />
            <code data-testid="s1-trial-launch-command">{launchCommand}</code>
          </div>
        </article>

        <article className="s1-artifact-panel s1-trial-material-panel">
          <div className="s1-panel-title">
            <FileText aria-hidden="true" size={18} />
            <h2>材料状态</h2>
          </div>
          <ul className="s1-trial-material-list" aria-label="评审材料状态">
            {materialStatus.map(([label, state]) => (
              <li key={label}>
                <CheckCircle2 aria-hidden="true" size={17} />
                <div>
                  <span>{label}</span>
                  <strong>{state}</strong>
                </div>
              </li>
            ))}
          </ul>
        </article>
      </section>

      <details className="s1-artifact-panel s1-trial-technical-details">
        <summary>技术对账信息</summary>
        <div className="s1-trial-split-grid">
          <dl className="s1-trial-launch-facts">
            <div>
              <dt>路由</dt>
              <dd data-testid="s1-trial-route">{trial.route}</dd>
            </div>
            <div>
              <dt>本地 URL</dt>
              <dd data-testid="s1-trial-local-url">{trial.localUrl}</dd>
            </div>
            <div>
              <dt>启动脚本</dt>
              <dd data-testid="s1-trial-launcher-script">{trial.launcherScript}</dd>
            </div>
            <div>
              <dt>启动记录</dt>
              <dd>{trial.launcherOutputPath}</dd>
            </div>
          </dl>
          <dl className="s1-trial-package-facts">
            <div>
              <dt>评审包</dt>
              <dd data-testid="s1-trial-package-path">{trial.packagePath}</dd>
            </div>
            <div>
              <dt>中文入口</dt>
              <dd data-testid="s1-trial-start-here-path">{trial.startHerePath}</dd>
            </div>
            <div>
              <dt>检查清单</dt>
              <dd>{trial.reviewerChecklistPath}</dd>
            </div>
            <div>
              <dt>反馈模板</dt>
              <dd>{trial.feedbackTemplatePath}</dd>
            </div>
          </dl>
        </div>
      </details>

      <section
        aria-labelledby="s1-trial-walkthrough-title"
        className="s1-artifact-panel"
        data-testid="s1-trial-walkthrough"
      >
        <div className="s1-panel-title">
          <ClipboardCheck aria-hidden="true" size={18} />
          <h2 id="s1-trial-walkthrough-title">试用流程</h2>
        </div>
        <ol className="s1-trial-steps">
          {trial.steps.map((step, index) => (
            <li data-testid="s1-trial-step" key={step.id}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{step.title}</strong>
                <p>{step.detail}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section
        aria-labelledby="s1-feedback-title"
        className="s1-artifact-panel s1-feedback-panel"
        data-artifact-write="false"
        data-backend-write="false"
        data-connector-call="false"
        data-customer-visible-output="false"
        data-production-writeback="false"
        data-qwen-api-call="false"
        data-testid="s1-feedback-panel"
      >
        <div className="s1-panel-title">
          <MessageSquareText aria-hidden="true" size={18} />
          <h2 id="s1-feedback-title">本地反馈</h2>
        </div>
        <div className="s1-feedback-layout">
          <div className="s1-feedback-controls">
            <div aria-label="本地反馈结论" className="s1-feedback-options" role="group">
              {FEEDBACK_OPTIONS.map((option) => (
                <button
                  aria-pressed={feedbackDecision === option.decision}
                  className={feedbackDecision === option.decision ? "is-selected" : undefined}
                  data-testid="s1-feedback-option"
                  key={option.decision}
                  onClick={() => setFeedbackDecision(option.decision)}
                  type="button"
                >
                  <span>{option.label}</span>
                  <small>{option.description}</small>
                </button>
              ))}
            </div>
            <label className="s1-review-notes-field">
              <span>反馈备注</span>
              <textarea
                aria-label="本地试用反馈备注"
                data-testid="s1-feedback-notes"
                onChange={(event) => setFeedbackNotes(event.target.value)}
                value={feedbackNotes}
              />
            </label>
          </div>
          <div className="s1-review-record-preview" data-testid="s1-feedback-preview">
            {JSON.stringify(feedbackPreview, null, 2)
              .split("\n")
              .map((line, index) => (
                <code key={`${index}-${line}`}>{line}</code>
              ))}
          </div>
        </div>
      </section>

      <section
        aria-labelledby="s1-qwen-contract-title"
        className="s1-artifact-panel"
        data-active-provider-mode={qwenContract.activeMode}
        data-connector-call-allowed={String(qwenContract.connectorCallAllowed)}
        data-live-call-allowed={String(qwenContract.liveCallAllowed)}
        data-testid="s1-qwen-provider-contract"
      >
        <div className="s1-panel-title">
          <Lock aria-hidden="true" size={18} />
          <h2 id="s1-qwen-contract-title">Qwen 接入状态</h2>
        </div>
        <dl className="s1-trial-package-facts">
          <div>
            <dt>当前模式</dt>
            <dd data-testid="s1-qwen-active-mode">{qwenContract.activeMode}</dd>
          </div>
          <div>
            <dt>Contract</dt>
            <dd>{qwenContract.configRef}</dd>
          </div>
        </dl>
        <div className="s1-provider-mode-grid">
          {qwenContract.modes.map((mode) => (
            <article data-provider-mode={mode.mode} data-testid="s1-qwen-provider-mode" key={mode.mode}>
              <strong>{mode.label}</strong>
              <span>{mode.status === "available" ? "可用" : "未启用"}</span>
              <p>{mode.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="s1-artifact-panel">
        <div className="s1-panel-title">
          <CheckCircle2 aria-hidden="true" size={18} />
          <h2>安全边界</h2>
        </div>
        <dl className="s1-trial-boundary-grid">
          {boundaryFacts.map(([label, value]) => (
            <div key={label}>
              <dt>{label}</dt>
              <dd>{yesNo(value)}</dd>
            </div>
          ))}
        </dl>
      </section>
    </section>
  );
}
