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
import { S1_QWEN_PROVIDER_DRY_PREVIEW } from "./s1QwenProviderDryPreview";
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
  const qwenDryPreview = S1_QWEN_PROVIDER_DRY_PREVIEW;
  const [feedbackDecision, setFeedbackDecision] = useState<FeedbackDecision>(
    "READY_FOR_NEXT_INTERNAL_TRIAL"
  );
  const [feedbackNotes, setFeedbackNotes] = useState(
    "评审者可以从 README、manifest、final_status、安全扫描和截图完成本地离线检查。"
  );
  const launchCommand = `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ${trial.launcherScript}`;
  const roleEntries = [
    {
      title: "一线研判",
      question: "我现在最应该先看哪件事?",
      description: "先看结论、影响和下一步，快速判断是否需要继续跟进。",
      action: "/incident/CASE-2847"
    },
    {
      title: "深度分析",
      question: "为什么这么判断?",
      description: "展开证据链、限制说明和推理计划，确认系统没有越过证据边界。",
      action: "展开可信证据"
    },
    {
      title: "管理审阅",
      question: "是否可以进入下一步?",
      description: "用管理视角看风险、人工确认状态、审阅结论和未关闭建议。",
      action: "查看试用结论"
    },
    {
      title: "部署与集成",
      question: "怎么启动和交付?",
      description: "查看本地启动、评审包、干运行模型契约和后续私有化部署路径。",
      action: "查看部署准备"
    }
  ];
  const productHomeFacts = [
    {
      label: "当前结论",
      value: "可继续内部本地试用",
      detail: "带备注通过，不代表客户发布或生产部署 GO。"
    },
    {
      label: "可信依据",
      value: `${run.caseCount} 个合成案例`,
      detail: "安全扫描零命中，证据链和限制说明可核验。"
    },
    {
      label: "建议动作",
      value: "先看结果页，再提交反馈",
      detail: "客户可见发布、真实数据和生产写回仍未授权。"
    }
  ];
  const nextActions = [
    {
      title: "查看试用结果",
      description: "进入结果页，先读中文结论、可信边界和下一步。",
      value: "/incident/CASE-2847"
    },
    {
      title: "提交本地反馈",
      description: "按准确性、可用性、缺失信息记录 reviewer 反馈。",
      value: "本地反馈预览"
    },
    {
      title: "查看部署准备",
      description: "确认启动脚本、评审包和 dry provider 状态。",
      value: trial.deliveryPackagePath
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
  const trustFacts = [
    "本轮只读取本地合成包",
    "不连接真实系统和 live Qwen/API",
    "不写回生产, 不发布客户可见输出",
    "技术对账信息默认下沉, 需要时再展开"
  ];
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
      <header className="s1-trial-header s1-product-home-hero">
        <div>
          <p className="summary-kicker">产品首页 / 内部本地试用</p>
          <h1 id="s1-trial-title">SecuPilot 企业安全分析助理</h1>
          <p className="s1-trial-lede">
            SecuPilot 把安全事件、证据链、模型建议和人工确认流程整理成一份可读结论，
            帮一线工程师、深度分析师、管理者和部署负责人判断现在该做什么。
          </p>
          <div className="s1-product-home-actions" aria-label="产品首页快捷动作">
            <a href="/incident/CASE-2847">查看事件研判</a>
            <a href="#s1-feedback-title">提交本地反馈</a>
            <a href="#s1-qwen-contract-title">查看部署准备</a>
          </div>
          <dl className="s1-trial-header-facts s1-product-home-summary-facts">
            {productHomeFacts.map((fact) => (
              <div key={fact.label}>
                <dt>{fact.label}</dt>
                <dd>{fact.value}</dd>
                <p>{fact.detail}</p>
              </div>
            ))}
          </dl>
        </div>
        <span className="s1-trial-status">
          <ShieldCheck aria-hidden="true" size={18} />
          本地离线 / 合成包
        </span>
      </header>

      <section
        aria-labelledby="s1-product-role-title"
        className="s1-product-home-section"
      >
        <div className="s1-product-home-section-heading">
          <p className="summary-kicker">角色入口</p>
          <h2 id="s1-product-role-title">按你的工作目标进入</h2>
        </div>
        <div className="s1-product-entry-grid s1-role-entry-grid" data-testid="s1-product-role-grid">
        {roleEntries.map((entry, index) => (
          <article data-testid="s1-product-role-entry" key={entry.title}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <div>
              <strong>{entry.title}</strong>
              <p>{entry.question}</p>
              <small>{entry.description}</small>
              <code>{entry.action}</code>
            </div>
            <ArrowRight aria-hidden="true" size={18} />
          </article>
        ))}
        </div>
      </section>

      <section aria-label="本地离线试用概览" className="s1-trial-kpi-grid">
        <article>
          <span>判断对象</span>
          <strong>{run.caseCount}</strong>
          <p>合成安全案例, 用于内部产品体验验证。</p>
        </article>
        <article>
          <span>安全扫描</span>
          <strong>{run.safetyScan.findingCount}</strong>
          <p>{`${run.safetyScan.scannedStringValues} 个字符串已扫描, 未发现敏感留存。`}</p>
        </article>
        <article>
          <span>云端模型</span>
          <strong>{yesNo(run.qwenUsed)}</strong>
          <p>当前只展示 dry contract, 不发起 live 调用。</p>
        </article>
        <article>
          <span>客户发布</span>
          <strong>{yesNo(run.canDeployToCustomerProduction)}</strong>
          <p>当前只用于内部本地试用, 不发布客户可见输出。</p>
        </article>
      </section>

      <section className="s1-trial-product-grid" aria-label="产品首页主要路径">
        <article className="s1-artifact-panel s1-assistant-plan-panel">
          <div className="s1-panel-title">
            <ShieldCheck aria-hidden="true" size={18} />
            <h2>SecuPilot 研判计划</h2>
          </div>
          <p>
            当前版本把告警理解、证据约束、人工确认和反馈闭环放在同一个产品路径里。
            它会先给结论, 再说明依据和不能确认的部分。
          </p>
          <ul className="s1-assistant-plan-list">
            <li>
              <strong>先判断</strong>
              <span>把事件结论、风险和下一步放在第一屏。</span>
            </li>
            <li>
              <strong>再解释</strong>
              <span>证据链、限制和技术对账默认折叠, 需要时展开。</span>
            </li>
            <li>
              <strong>后交接</strong>
              <span>反馈、报告、评审包和部署准备都保留本地离线边界。</span>
            </li>
          </ul>
        </article>

        <article className="s1-artifact-panel s1-trust-strip-panel">
          <div className="s1-panel-title">
            <CheckCircle2 aria-hidden="true" size={18} />
            <h2>为什么可信</h2>
          </div>
          <ul className="s1-trust-strip" data-testid="s1-product-trust-strip">
            {trustFacts.map((fact) => (
              <li key={fact}>
                <CheckCircle2 aria-hidden="true" size={16} />
                <span>{fact}</span>
              </li>
            ))}
          </ul>
        </article>
      </section>

      <section
        aria-labelledby="s1-product-next-actions-title"
        className="s1-product-home-section"
      >
        <div className="s1-product-home-section-heading">
          <p className="summary-kicker">下一步</p>
          <h2 id="s1-product-next-actions-title">先完成一次内部试用闭环</h2>
        </div>
        <div className="s1-product-entry-grid">
          {nextActions.map((action, index) => (
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
        </div>
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
          <dl className="s1-trial-header-facts s1-product-home-technical-facts">
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
        <div
          className="s1-qwen-dry-preview"
          data-autonomous-qwen-action={String(qwenDryPreview.boundaries.autonomousQwenAction)}
          data-customer-visible-output={String(qwenDryPreview.boundaries.customerVisibleOutput)}
          data-live-connectors={String(qwenDryPreview.boundaries.liveConnectors)}
          data-live-qwen-api={String(qwenDryPreview.boundaries.liveQwenApi)}
          data-production-writeback={String(qwenDryPreview.boundaries.productionWriteback)}
          data-provider-mode={qwenDryPreview.providerMode}
          data-secret-material-allowed={String(qwenDryPreview.boundaries.secretMaterialAllowed)}
          data-testid="s1-qwen-dry-preview"
        >
          <div>
            <strong>Dry provider 输入预览</strong>
            <dl className="s1-trial-package-facts">
              <div>
                <dt>数据模式</dt>
                <dd data-testid="s1-qwen-dry-data-mode">{qwenDryPreview.dataMode}</dd>
              </div>
              <div>
                <dt>本地 fixture</dt>
                <dd>{qwenDryPreview.fixtureSourceRef}</dd>
              </div>
              <div>
                <dt>输入包</dt>
                <dd>{qwenDryPreview.inputPackageRef}</dd>
              </div>
              <div>
                <dt>案例数</dt>
                <dd>{qwenDryPreview.caseCount}</dd>
              </div>
            </dl>
          </div>
          <div>
            <strong>Dry provider 输出预览</strong>
            <dl className="s1-trial-package-facts">
              <div>
                <dt>案例</dt>
                <dd data-testid="s1-qwen-dry-case-id">{qwenDryPreview.outputPreview.caseId}</dd>
              </div>
              <div>
                <dt>风险</dt>
                <dd>{qwenDryPreview.outputPreview.riskLevel}</dd>
              </div>
              <div>
                <dt>人工动作</dt>
                <dd data-testid="s1-qwen-dry-reviewer-action">
                  {qwenDryPreview.outputPreview.reviewerAction}
                </dd>
              </div>
              <div>
                <dt>置信度</dt>
                <dd>{qwenDryPreview.outputPreview.confidence}</dd>
              </div>
            </dl>
            <p data-testid="s1-qwen-dry-model-summary">
              {qwenDryPreview.outputPreview.modelSummary}
            </p>
          </div>
          <div>
            <strong>拒绝进入 UI 的字段</strong>
            <ul className="s1-qwen-rejected-fields">
              {qwenDryPreview.rejectedFieldLabels.map((label) => (
                <li key={label}>{label}</li>
              ))}
            </ul>
          </div>
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
