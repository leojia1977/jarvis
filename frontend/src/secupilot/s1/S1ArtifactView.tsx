import { useMemo, useState } from "react";
import { Activity, ClipboardCheck, FileText, Lock, ShieldCheck } from "lucide-react";
import {
  S1_CLOSED_SHADOW_RUN_ARTIFACTS,
  type S1LocalReviewDecision
} from "./s1ClosedShadowRunArtifacts";

function yesNo(value: boolean): string {
  return value ? "YES" : "NO";
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
      label: "Customer visible output",
      value: run.boundaries.customerVisibleOutput,
      testId: "s1-customer-visible-output"
    },
    {
      label: "Production write-back",
      value: run.boundaries.productionWriteback,
      testId: "s1-production-writeback"
    },
    {
      label: "Production connectors",
      value: run.boundaries.productionConnectors,
      testId: "s1-production-connectors"
    },
    {
      label: "Qwen autonomous action",
      value: run.boundaries.qwenAutonomousAction,
      testId: "s1-qwen-autonomy"
    },
    {
      label: "Raw payload retained",
      value: run.boundaries.rawPayloadRetention,
      testId: "s1-raw-payload-retained"
    },
    {
      label: "Secret retained",
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
          <p className="summary-kicker">S1 artifact viewer</p>
          <h1 id="s1-artifact-title">S1 Closed Shadow Run</h1>
          <dl className="s1-run-header-facts">
            <div>
              <dt>Run ID</dt>
              <dd data-testid="s1-run-id">{run.runId}</dd>
            </div>
            <div>
              <dt>GO record</dt>
              <dd>{run.goRecordRef}</dd>
            </div>
            <div>
              <dt>Data mode</dt>
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
          <span>Provider</span>
          <strong data-testid="s1-provider">{run.provider}</strong>
          <p>{run.inputKind}</p>
        </article>
        <article>
          <span>Cases</span>
          <strong data-testid="s1-case-count">{run.caseCount}</strong>
          <p>{run.inputRef}</p>
        </article>
        <article>
          <span>Safety findings</span>
          <strong data-testid="s1-safety-finding-count">
            {run.safetyScan.findingCount}
          </strong>
          <p>{`${run.safetyScan.scannedStringValues} strings scanned`}</p>
        </article>
        <article>
          <span>Qwen used</span>
          <strong data-testid="s1-qwen-used">{yesNo(run.qwenUsed)}</strong>
          <p>{run.reviewerAction}</p>
        </article>
      </section>

      <section className="s1-split-grid">
        <article className="s1-artifact-panel">
          <div className="s1-panel-title">
            <Lock aria-hidden="true" size={18} />
            <h2>Runtime Boundaries</h2>
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
            <h2>Run Status</h2>
          </div>
          <dl className="s1-status-facts">
            <div>
              <dt>Exit code</dt>
              <dd>{run.exitCode}</dd>
            </div>
            <div>
              <dt>Next step</dt>
              <dd>{run.nextStep}</dd>
            </div>
            <div>
              <dt>Local demo</dt>
              <dd data-testid="s1-local-demo">{yesNo(run.canShowInLocalDemo)}</dd>
            </div>
            <div>
              <dt>Customer production deploy</dt>
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
          <h2 id="s1-local-review-title">Local Review Decision</h2>
        </div>
        <div className="s1-review-layout">
          <div className="s1-review-controls">
            <div className="s1-review-current">
              <span>Candidate</span>
              <strong>{run.localReview.candidate}</strong>
            </div>
            <div
              aria-label="Local review decision options"
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
              <span>Reviewer notes</span>
              <textarea
                aria-label="Reviewer notes"
                data-testid="s1-review-notes"
                onChange={(event) => setReviewNotes(event.target.value)}
                value={reviewNotes}
              />
            </label>
          </div>
          <div className="s1-review-preview">
            <dl className="s1-review-facts">
              <div>
                <dt>Selected decision</dt>
                <dd data-testid="s1-selected-review-decision">{reviewDecision}</dd>
              </div>
              <div>
                <dt>Preview scope</dt>
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
          <h2 id="s1-review-handoff-title">Offline Review Handoff</h2>
        </div>
        <dl className="s1-handoff-facts">
          <div>
            <dt>Package</dt>
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
            <dt>Mode</dt>
            <dd data-testid="s1-review-mode">{run.localReview.handoff.reviewMode}</dd>
          </div>
        </dl>
        <div className="s1-handoff-grid">
          <div>
            <h3>Reviewer Checks</h3>
            <ul>
              {run.localReview.handoff.requiredChecks.map((item) => (
                <li data-testid="s1-review-required-check" key={item}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3>Boundary Checks</h3>
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
          <h2>Artifact Manifest</h2>
        </div>
        <div className="s1-table-shell">
          <table className="s1-artifact-table">
            <thead>
              <tr>
                <th scope="col">File</th>
                <th scope="col">Retention</th>
                <th scope="col">SHA256</th>
                <th scope="col">Raw</th>
                <th scope="col">Secret</th>
                <th scope="col">Customer</th>
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
          <h2>Case Summary</h2>
        </div>
        <div className="s1-table-shell">
          <table className="s1-case-table">
            <thead>
              <tr>
                <th scope="col">Case</th>
                <th scope="col">Title</th>
                <th scope="col">Source</th>
                <th scope="col">Decision</th>
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
