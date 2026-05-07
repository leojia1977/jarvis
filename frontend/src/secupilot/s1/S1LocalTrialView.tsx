import { ClipboardCheck, FileText, Lock, MonitorCheck, PlayCircle, ShieldCheck } from "lucide-react";
import { S1_CLOSED_SHADOW_RUN_ARTIFACTS } from "./s1ClosedShadowRunArtifacts";

function yesNo(value: boolean): string {
  return value ? "YES" : "NO";
}

export function S1LocalTrialView() {
  const run = S1_CLOSED_SHADOW_RUN_ARTIFACTS;
  const trial = run.localTrial;
  const launchCommand = `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ${trial.launcherScript}`;
  const boundaryFacts = [
    ["Real data", false],
    ["Masked-real data", false],
    ["Live Qwen/API", false],
    ["Live connectors", false],
    ["Production write-back", run.boundaries.productionWriteback],
    ["Customer-visible output", run.boundaries.customerVisibleOutput],
    ["Push", false]
  ] as const;

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
          <p className="summary-kicker">Local offline trial</p>
          <h1 id="s1-trial-title">S1 Reviewer Walkthrough</h1>
          <dl className="s1-trial-header-facts">
            <div>
              <dt>Candidate</dt>
              <dd data-testid="s1-trial-candidate">{trial.candidate}</dd>
            </div>
            <div>
              <dt>Readiness</dt>
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
          Internal local/offline only
        </span>
      </header>

      <section aria-label="Local offline trial facts" className="s1-trial-kpi-grid">
        <article>
          <span>Cases</span>
          <strong>{run.caseCount}</strong>
          <p>{run.inputRef}</p>
        </article>
        <article>
          <span>Safety findings</span>
          <strong>{run.safetyScan.findingCount}</strong>
          <p>{`${run.safetyScan.scannedStringValues} strings scanned`}</p>
        </article>
        <article>
          <span>Qwen used</span>
          <strong>{yesNo(run.qwenUsed)}</strong>
          <p>Fixture path only</p>
        </article>
        <article>
          <span>Deploy ready</span>
          <strong>{yesNo(run.canDeployToCustomerProduction)}</strong>
          <p>No customer-visible authority</p>
        </article>
      </section>

      <section className="s1-trial-split-grid">
        <article
          className="s1-artifact-panel s1-trial-launcher"
          data-testid="s1-trial-launcher-panel"
        >
          <div className="s1-panel-title">
            <PlayCircle aria-hidden="true" size={18} />
            <h2>MVP-14 Launcher</h2>
          </div>
          <dl className="s1-trial-launch-facts">
            <div>
              <dt>Route</dt>
              <dd data-testid="s1-trial-route">{trial.route}</dd>
            </div>
            <div>
              <dt>Local URL</dt>
              <dd data-testid="s1-trial-local-url">{trial.localUrl}</dd>
            </div>
            <div>
              <dt>Launcher</dt>
              <dd data-testid="s1-trial-launcher-script">{trial.launcherScript}</dd>
            </div>
            <div>
              <dt>Launch info</dt>
              <dd>{trial.launcherOutputPath}</dd>
            </div>
          </dl>
          <div className="s1-launch-command" aria-label="Local trial launch command">
            <MonitorCheck aria-hidden="true" size={18} />
            <code data-testid="s1-trial-launch-command">{launchCommand}</code>
          </div>
        </article>

        <article className="s1-artifact-panel">
          <div className="s1-panel-title">
            <FileText aria-hidden="true" size={18} />
            <h2>Package Entry</h2>
          </div>
          <dl className="s1-trial-package-facts">
            <div>
              <dt>Package</dt>
              <dd data-testid="s1-trial-package-path">{trial.packagePath}</dd>
            </div>
            <div>
              <dt>README</dt>
              <dd data-testid="s1-trial-readme-path">{trial.readmePath}</dd>
            </div>
            <div>
              <dt>Route decision</dt>
              <dd>{trial.routeDecisionDoc}</dd>
            </div>
            <div>
              <dt>RC-006 closeout</dt>
              <dd>{trial.closeoutDoc}</dd>
            </div>
          </dl>
        </article>
      </section>

      <section
        aria-labelledby="s1-trial-walkthrough-title"
        className="s1-artifact-panel"
        data-testid="s1-trial-walkthrough"
      >
        <div className="s1-panel-title">
          <ClipboardCheck aria-hidden="true" size={18} />
          <h2 id="s1-trial-walkthrough-title">MVP-15 Walkthrough</h2>
        </div>
        <ol className="s1-trial-steps">
          {trial.steps.map((step, index) => (
            <li data-testid="s1-trial-step" key={step.id}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{step.title}</strong>
                <p>{step.detail}</p>
                <code>{step.artifactRef}</code>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="s1-artifact-panel">
        <div className="s1-panel-title">
          <Lock aria-hidden="true" size={18} />
          <h2>Boundary Lock</h2>
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
