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
import { S1_QWEN_PROVIDER_READINESS } from "./s1QwenProviderReadiness";

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
  const qwenReadiness = S1_QWEN_PROVIDER_READINESS;
  const [feedbackDecision, setFeedbackDecision] = useState<FeedbackDecision>(
    "READY_FOR_NEXT_INTERNAL_TRIAL"
  );
  const [feedbackNotes, setFeedbackNotes] = useState(
    "评审者可以从 README、manifest、final_status、安全扫描和截图完成本地离线检查。"
  );
  const launchCommand = `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ${trial.launcherScript}`;
  const roleEntries = [
    {
      title: "工程师视角",
      question: "我现在最应该先看哪件事?",
      description: "先看事件结论、影响范围和建议动作，快速判断是否需要继续跟进。",
      action: "打开事件详情"
    },
    {
      title: "分析负责人视角",
      question: "为什么这么判断?",
      description: "展开证据链、限制说明和模型建议，确认判断没有越过证据边界。",
      action: "核对可信依据"
    },
    {
      title: "安全负责人视角",
      question: "是否可以进入下一步?",
      description: "用管理视角看风险、人工确认状态、试用结论和未关闭建议。",
      action: "查看结果摘要"
    },
    {
      title: "CTO / 部署视角",
      question: "怎么启动和交付?",
      description: "查看私有化部署前置条件、模型接入准备和本地启动方式。",
      action: "查看接入准备"
    }
  ];
  const productHomeFacts = [
    {
      label: "SecuPilot 是谁",
      value: "企业安全分析助理",
      detail: "把事件结论、可信依据和下一步建议整理给不同层级的使用者。"
    },
    {
      label: "帮我判断什么",
      value: "这起事件该怎么处理",
      detail: `${run.caseCount} 个合成案例用于验证判断链路，安全扫描零命中。`
    },
    {
      label: "现在建议做什么",
      value: "先看结论，再核依据，最后反馈",
      detail: "当前仍是本地安全预览，不连接真实系统，不写生产。"
    }
  ];
  const nextActions = [
    {
      title: "查看试用结果",
      description: "进入结果页，先读中文结论、可信边界和下一步。",
      value: "打开事件研判结果"
    },
    {
      title: "提交本地反馈",
      description: "按准确性、可用性、缺失信息记录 reviewer 反馈。",
      value: "记录试用体验"
    },
    {
      title: "查看部署准备",
      description: "确认启动脚本、评审包和 dry provider 状态。",
      value: "核对私有化前置条件"
    }
  ];
  const privatePreviewRoutes = [
    {
      label: "01",
      title: "试用首页",
      route: "/s1-trial",
      audience: "所有角色",
      outcome: "先理解 SecuPilot 是谁、帮我判断什么、现在建议做什么。"
    },
    {
      label: "02",
      title: "事件研判",
      route: "/incident/CASE-2847",
      audience: "工程师 / 分析负责人",
      outcome: "查看结论、影响、可信依据、建议动作和反馈入口。"
    },
    {
      label: "03",
      title: "本地反馈",
      route: "页面内反馈区",
      audience: "试用 reviewer",
      outcome: "记录准确性、可用性和缺失信息，不写后端。"
    },
    {
      label: "04",
      title: "模型接入准备",
      route: "模型接入准备区",
      audience: "CTO / 部署负责人",
      outcome: "查看 Qwen synthetic provider readiness，确认仍是 no-network dry path。"
    },
    {
      label: "05",
      title: "技术对账",
      route: "按需展开",
      audience: "内部核验",
      outcome: "只在需要时核对 candidate、run、package、manifest 和边界。"
    }
  ];
  const privatePreviewChecklist = [
    ["启动入口", "本机浏览器打开 /s1-trial"],
    ["核心动作", "看事件研判并提交本地反馈"],
    ["模型路径", "只看 synthetic provider stub readiness"],
    ["交付边界", "不部署、不连真实系统、不产生客户可见输出"]
  ] as const;
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
  const homeQueueItems = [
    {
      status: "当前演示",
      title: "可疑横向移动事件",
      detail: "先看结论、影响范围和建议动作",
      tone: "active"
    },
    {
      status: "模型路径",
      title: "Qwen synthetic provider",
      detail: "只预览 dry-run/stub, 不发起 live 调用",
      tone: "model"
    },
    {
      status: "交付边界",
      title: "Windows 私有化预览",
      detail: "本地启动、离线反馈、人工确认",
      tone: "safe"
    }
  ];
  const homeStatusFacts = [
    ["当前包", "RC-019 中文预览"],
    ["案例数", `${run.caseCount}`],
    ["安全命中", `${run.safetyScan.findingCount}`],
    ["生产写回", yesNo(run.boundaries.productionWriteback)]
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
      <section className="s1-customer-product-home" data-testid="s1-customer-product-home">
        <header className="s1-trial-header s1-product-home-hero s1-customer-hero">
          <div className="s1-customer-hero-copy">
            <p className="summary-kicker">客户试用入口 / 私有化预览</p>
            <h1 id="s1-trial-title">SecuPilot 企业安全分析助理</h1>
            <p className="s1-trial-lede">
              给一线工程师到 CTO 的统一安全研判入口：先告诉你这起事件是否值得处理，
              再说明为什么可信、缺什么证据、下一步应该由谁确认。
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
          <aside className="s1-customer-command-card" aria-label="SecuPilot 当前预览状态">
            <span className="s1-trial-status">
              <ShieldCheck aria-hidden="true" size={18} />
              本地安全预览
            </span>
            <strong>第一眼先看产品判断，不看证据目录</strong>
            <p>
              这是客户进入后的产品首页：它负责引导试用路径；事件详情和技术对账在后续页面展开。
            </p>
            <dl>
              {homeStatusFacts.map(([label, value]) => (
                <div key={label}>
                  <dt>{label}</dt>
                  <dd>{value}</dd>
                </div>
              ))}
            </dl>
          </aside>
        </header>

        <div className="s1-customer-home-layout">
          <section
            aria-labelledby="s1-private-preview-shell-title"
            className="s1-private-preview-shell"
            data-testid="s1-private-preview-shell"
          >
            <div className="s1-product-home-section-heading">
              <p className="summary-kicker">私有化预览启动壳</p>
              <h2 id="s1-private-preview-shell-title">从一个入口完成试用、反馈和接入准备</h2>
              <p>
                当前预览像产品一样进入：打开首页、查看事件研判、提交本地反馈、确认模型接入准备。
                证据包和技术字段保留在后台对账区，不作为客户第一眼的主要内容。
              </p>
            </div>
            <div className="s1-private-preview-checklist" data-testid="s1-private-preview-checklist">
              {privatePreviewChecklist.map(([label, value]) => (
                <div key={label}>
                  <span>{label}</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
            <div className="s1-product-route-map" data-testid="s1-product-route-map">
              {privatePreviewRoutes.map((item) => (
                <article data-testid="s1-product-route-map-item" key={item.label}>
                  <span>{item.label}</span>
                  <div>
                    <strong>{item.title}</strong>
                    <small>{item.audience}</small>
                    <p>{item.outcome}</p>
                    <code>{item.route}</code>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <aside className="s1-customer-queue-panel" aria-label="SecuPilot 产品预览队列">
            <div>
              <p className="summary-kicker">产品预览队列</p>
              <h2>今天先验证这三段体验</h2>
            </div>
            <ol>
              {homeQueueItems.map((item) => (
                <li data-tone={item.tone} key={item.title}>
                  <span>{item.status}</span>
                  <strong>{item.title}</strong>
                  <p>{item.detail}</p>
                </li>
              ))}
            </ol>
          </aside>
        </div>

        <section
          aria-labelledby="s1-product-role-title"
          className="s1-product-home-section s1-customer-role-section"
        >
          <div className="s1-product-home-section-heading">
            <p className="summary-kicker">客户角色入口</p>
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
      </section>

      <section aria-label="本地离线试用概览" className="s1-trial-kpi-grid">
        <article>
          <span>演练案例</span>
          <strong>{run.caseCount}</strong>
          <p>用合成事件验证从结论到反馈的完整产品路径。</p>
        </article>
        <article>
          <span>安全扫描</span>
          <strong>{run.safetyScan.findingCount}</strong>
          <p>{`${run.safetyScan.scannedStringValues} 个字符串已扫描, 未发现敏感留存。`}</p>
        </article>
        <article>
          <span>模型接入</span>
          <strong>已演练</strong>
          <p>Qwen provider stub 已可本地预览, 仍不发起 live 调用。</p>
        </article>
        <article>
          <span>上线状态</span>
          <strong>{yesNo(run.canDeployToCustomerProduction)}</strong>
          <p>当前不是客户发布或生产部署, 只用于本地安全预览。</p>
        </article>
      </section>

      <section className="s1-trial-product-grid" aria-label="产品首页主要路径">
        <article className="s1-artifact-panel s1-assistant-plan-panel">
          <div className="s1-panel-title">
            <ShieldCheck aria-hidden="true" size={18} />
            <h2>SecuPilot 研判计划</h2>
          </div>
          <p>
            当前版本把告警理解、证据约束、建议动作、人工确认和反馈闭环放在同一个产品路径里。
            它先给结论, 再说明依据、限制和不能确认的部分。
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
              <span>反馈、报告、评审包和部署准备都保留本地安全边界。</span>
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
          <p className="summary-kicker">试用路径</p>
          <h2 id="s1-product-next-actions-title">一次试用要完成的三件事</h2>
        </div>
        <div className="s1-product-entry-grid">
          {nextActions.map((action, index) => (
            <article key={action.title}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{action.title}</strong>
                <p>{action.description}</p>
                <small>{action.value}</small>
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
            <h2>打开试用入口</h2>
          </div>
          <p>
            当前候选包已通过本地安全边界检查。先打开试用入口，再按材料状态完成核验。
          </p>
          <div className="s1-trial-primary-action">
            <span>本地入口</span>
            <strong>{trial.localUrl}</strong>
          </div>
          <details className="s1-launch-command" aria-label="本地试用启动命令">
            <summary>
              <MonitorCheck aria-hidden="true" size={18} />
              一键启动脚本
            </summary>
            <code data-testid="s1-trial-launch-command">{launchCommand}</code>
          </details>
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
        data-network-call={String(qwenReadiness.boundaries.networkCall)}
        data-provider-stub-ready="true"
        data-provider-stub-status={qwenReadiness.status}
        data-secret-values-read={String(qwenReadiness.boundaries.secretValuesRead)}
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
            <dt>接入状态</dt>
            <dd data-testid="s1-qwen-readiness-status">{qwenReadiness.productLabel}</dd>
          </div>
          <div>
            <dt>合成案例</dt>
            <dd data-testid="s1-qwen-readiness-case-count">{qwenReadiness.caseCount}</dd>
          </div>
          <div>
            <dt>Contract</dt>
            <dd>{qwenContract.configRef}</dd>
          </div>
        </dl>
        <article className="s1-qwen-readiness-card" data-testid="s1-qwen-readiness-card">
          <strong>{qwenReadiness.productLabel}</strong>
          <p>{qwenReadiness.productDescription}</p>
          <dl className="s1-trial-package-facts">
            <div>
              <dt>provider stub</dt>
              <dd data-testid="s1-qwen-provider-stub-mode">{qwenReadiness.providerStubMode}</dd>
            </div>
            <div>
              <dt>输出报告</dt>
              <dd>{qwenReadiness.providerReportRef}</dd>
            </div>
            <div>
              <dt>下一步</dt>
              <dd>{qwenReadiness.nextStep}</dd>
            </div>
          </dl>
        </article>
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
