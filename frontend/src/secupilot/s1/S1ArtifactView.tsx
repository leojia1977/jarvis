import { useMemo, useState } from "react";
import { Activity, ClipboardCheck, FileText, Lock, ShieldCheck } from "lucide-react";
import {
  S1_CLOSED_SHADOW_RUN_ARTIFACTS,
  type S1LocalReviewDecision
} from "./s1ClosedShadowRunArtifacts";

function yesNo(value: boolean): string {
  return value ? "是" : "否";
}

function shaShort(value: string): string {
  return value.slice(0, 12);
}

export function S1ArtifactView() {
  const run = S1_CLOSED_SHADOW_RUN_ARTIFACTS;
  const [reviewDecision, setReviewDecision] = useState<S1LocalReviewDecision>(
    run.localReview.defaultDecision
  );
  const [reviewNotes, setReviewNotes] = useState<string>(run.localReview.defaultNotes);

  const localReviewRecord = useMemo(
    () => ({
      schema_version: run.localReview.schemaVersion,
      candidate: run.localReview.candidate,
      source_candidate: run.localReview.sourceCandidate,
      run_id: run.runId,
      reviewer: run.localReview.reviewer,
      decision: reviewDecision,
      notes: reviewNotes,
      record_scope: "LOCAL_BROWSER_PREVIEW_ONLY",
      state_mutation: "none",
      artifact_write: false,
      qwen_api_call: false,
      connector_call: false,
      customer_visible_output: false,
      production_writeback: false
    }),
    [
      reviewDecision,
      reviewNotes,
      run.localReview.candidate,
      run.localReview.reviewer,
      run.localReview.schemaVersion,
      run.localReview.sourceCandidate,
      run.runId
    ]
  );

  const boundaryFacts = [
    {
      label: "客户可见输出",
      value: run.boundaries.customerVisibleOutput,
      testId: "s1-customer-visible-output"
    },
    {
      label: "生产写回",
      value: run.boundaries.productionWriteback,
      testId: "s1-production-writeback"
    },
    {
      label: "生产 connector",
      value: run.boundaries.productionConnectors,
      testId: "s1-production-connectors"
    },
    {
      label: "Qwen 自主动作",
      value: run.boundaries.qwenAutonomousAction,
      testId: "s1-qwen-autonomy"
    },
    {
      label: "原始载荷留存",
      value: run.boundaries.rawPayloadRetention,
      testId: "s1-raw-payload-retained"
    },
    {
      label: "密钥留存",
      value: run.boundaries.secretRetention,
      testId: "s1-secret-retained"
    }
  ];

  return (
    <section
      aria-labelledby="s1-artifact-title"
      className="page-region s1-artifact-view"
      data-artifact-source="static-mvp-fixture"
      data-customer-visible-output={String(run.boundaries.customerVisibleOutput)}
      data-production-writeback={String(run.boundaries.productionWriteback)}
      data-qwen-used={String(run.qwenUsed)}
      data-runtime-source="none"
      data-testid="s1-artifact-view"
    >
      <header className="s1-run-header">
        <div>
          <p className="summary-kicker">S1 证据查看器</p>
          <h1 id="s1-artifact-title">S1 Closed Shadow 运行证据</h1>
          <dl className="s1-run-header-facts">
            <div>
              <dt>Run ID</dt>
              <dd data-testid="s1-run-id">{run.runId}</dd>
            </div>
            <div>
              <dt>GO 记录</dt>
              <dd>{run.goRecordRef}</dd>
            </div>
            <div>
              <dt>数据模式</dt>
              <dd>{run.dataMode}</dd>
            </div>
          </dl>
        </div>
        <span className="s1-status-pill" data-testid="s1-final-outcome">
          <ShieldCheck aria-hidden="true" size={18} />
          {run.finalOutcome}
        </span>
      </header>

      <section aria-label="S1 run facts" className="s1-kpi-grid">
        <article>
          <span>提供方</span>
          <strong data-testid="s1-provider">{run.provider}</strong>
          <p>{run.inputKind}</p>
        </article>
        <article>
          <span>案例数</span>
          <strong data-testid="s1-case-count">{run.caseCount}</strong>
          <p>{run.inputRef}</p>
        </article>
        <article>
          <span>安全扫描命中</span>
          <strong data-testid="s1-safety-finding-count">
            {run.safetyScan.findingCount}
          </strong>
          <p>{`${run.safetyScan.scannedStringValues} 个字符串已扫描`}</p>
        </article>
        <article>
          <span>Qwen 调用</span>
          <strong data-testid="s1-qwen-used">{yesNo(run.qwenUsed)}</strong>
          <p>{run.reviewerAction}</p>
        </article>
      </section>

      <section className="s1-split-grid">
        <article className="s1-artifact-panel">
          <div className="s1-panel-title">
            <Lock aria-hidden="true" size={18} />
            <h2>运行边界</h2>
          </div>
          <dl className="s1-boundary-grid">
            {boundaryFacts.map((fact) => (
              <div key={fact.testId}>
                <dt>{fact.label}</dt>
                <dd data-testid={fact.testId}>{yesNo(fact.value)}</dd>
              </div>
            ))}
          </dl>
        </article>

        <article className="s1-artifact-panel">
          <div className="s1-panel-title">
            <Activity aria-hidden="true" size={18} />
            <h2>运行状态</h2>
          </div>
          <dl className="s1-status-facts">
            <div>
              <dt>退出码</dt>
              <dd>{run.exitCode}</dd>
            </div>
            <div>
              <dt>下一步</dt>
              <dd>{run.nextStep}</dd>
            </div>
            <div>
              <dt>本地演示</dt>
              <dd data-testid="s1-local-demo">{yesNo(run.canShowInLocalDemo)}</dd>
            </div>
            <div>
              <dt>客户生产部署</dt>
              <dd data-testid="s1-production-deploy">
                {yesNo(run.canDeployToCustomerProduction)}
              </dd>
            </div>
          </dl>
          <p data-testid="s1-pass-hold-reason">{run.passHoldReason}</p>
        </article>
      </section>

      <section
        aria-labelledby="s1-local-review-title"
        className="s1-artifact-panel s1-review-panel"
        data-artifact-write="false"
        data-connector-call="false"
        data-customer-visible-output="false"
        data-production-writeback="false"
        data-qwen-api-call="false"
        data-review-scope={run.localReview.candidate}
        data-source-candidate={run.localReview.sourceCandidate}
        data-state-mutation="none"
        data-testid="s1-local-review-panel"
      >
        <div className="s1-panel-title">
          <ClipboardCheck aria-hidden="true" size={18} />
          <h2 id="s1-local-review-title">本地评审决定</h2>
        </div>
        <div className="s1-review-layout">
          <div className="s1-review-controls">
            <div className="s1-review-current">
              <span>候选版本</span>
              <strong>{run.localReview.candidate}</strong>
            </div>
            <div
              aria-label="本地评审决定选项"
              className="s1-review-decision-grid"
              role="group"
            >
              {run.localReview.allowedDecisions.map((decision) => (
                <button
                  aria-pressed={decision === reviewDecision}
                  className={decision === reviewDecision ? "is-selected" : undefined}
                  data-decision={decision}
                  data-testid="s1-review-decision-option"
                  key={decision}
                  onClick={() => setReviewDecision(decision)}
                  type="button"
                >
                  {decision}
                </button>
              ))}
            </div>
            <label className="s1-review-notes-field">
              <span>评审备注</span>
              <textarea
                aria-label="评审备注"
                data-testid="s1-review-notes"
                onChange={(event) => setReviewNotes(event.target.value)}
                value={reviewNotes}
              />
            </label>
          </div>
          <div className="s1-review-preview">
            <dl className="s1-review-facts">
              <div>
                <dt>已选决定</dt>
                <dd data-testid="s1-selected-review-decision">{reviewDecision}</dd>
              </div>
              <div>
                <dt>预览范围</dt>
                <dd>LOCAL_BROWSER_PREVIEW_ONLY</dd>
              </div>
            </dl>
            <div className="s1-review-record-preview" data-testid="s1-review-record-preview">
              {JSON.stringify(localReviewRecord, null, 2)
                .split("\n")
                .map((line, index) => (
                  <code key={`${index}-${line}`}>{line}</code>
                ))}
            </div>
          </div>
        </div>
      </section>

      <section
        aria-labelledby="s1-review-handoff-title"
        className="s1-artifact-panel s1-handoff-panel"
        data-connector-call="false"
        data-customer-visible-output="false"
        data-production-writeback="false"
        data-qwen-api-call="false"
        data-review-mode={run.localReview.handoff.reviewMode}
        data-review-package={run.localReview.handoff.packagePath}
        data-review-readme={run.localReview.handoff.readmePath}
        data-state-mutation="none"
        data-testid="s1-review-handoff-panel"
      >
        <div className="s1-panel-title">
          <FileText aria-hidden="true" size={18} />
          <h2 id="s1-review-handoff-title">离线评审交接</h2>
        </div>
        <dl className="s1-handoff-facts">
          <div>
            <dt>评审包</dt>
            <dd data-testid="s1-review-package-path">{run.localReview.handoff.packagePath}</dd>
          </div>
          <div>
            <dt>README</dt>
            <dd data-testid="s1-review-readme-path">{run.localReview.handoff.readmePath}</dd>
          </div>
          <div>
            <dt>ZIP</dt>
            <dd data-testid="s1-review-zip-name">{run.localReview.handoff.zipName}</dd>
          </div>
          <div>
            <dt>模式</dt>
            <dd data-testid="s1-review-mode">{run.localReview.handoff.reviewMode}</dd>
          </div>
        </dl>
        <div className="s1-handoff-grid">
          <div>
            <h3>评审检查项</h3>
            <ul>
              {run.localReview.handoff.requiredChecks.map((item) => (
                <li data-testid="s1-review-required-check" key={item}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3>边界检查项</h3>
            <ul>
              {run.localReview.handoff.boundaryChecks.map((item) => (
                <li data-testid="s1-review-boundary-check" key={item}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="s1-artifact-panel">
        <div className="s1-panel-title">
          <FileText aria-hidden="true" size={18} />
          <h2>Artifact 清单</h2>
        </div>
        <div className="s1-table-shell">
          <table className="s1-artifact-table">
            <thead>
              <tr>
                <th scope="col">文件</th>
                <th scope="col">留存级别</th>
                <th scope="col">SHA256</th>
                <th scope="col">原始载荷</th>
                <th scope="col">密钥</th>
                <th scope="col">客户可见</th>
              </tr>
            </thead>
            <tbody>
              {run.artifacts.map((artifact) => (
                <tr data-testid="s1-artifact-row" key={artifact.fileName}>
                  <td>
                    <strong>{artifact.fileName}</strong>
                    <span>{artifact.path}</span>
                  </td>
                  <td>{artifact.retentionClass}</td>
                  <td>{shaShort(artifact.sha256)}</td>
                  <td>{yesNo(artifact.containsRawPayload)}</td>
                  <td>{yesNo(artifact.containsSecretOrToken)}</td>
                  <td>{yesNo(artifact.containsCustomerVisibleArtifact)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="s1-artifact-panel">
        <div className="s1-panel-title">
          <ShieldCheck aria-hidden="true" size={18} />
          <h2>案例摘要</h2>
        </div>
        <div className="s1-table-shell">
          <table className="s1-case-table">
            <thead>
              <tr>
                <th scope="col">案例</th>
                <th scope="col">标题</th>
                <th scope="col">来源</th>
                <th scope="col">决定</th>
              </tr>
            </thead>
            <tbody>
              {run.cases.map((item) => (
                <tr data-testid="s1-case-row" key={item.caseId}>
                  <td>{item.caseId}</td>
                  <td>{item.title}</td>
                  <td>{item.sourceId}</td>
                  <td>{item.decisionHint}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}
