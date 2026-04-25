import { SecurityHaltCode } from "../context/types";

type SecurityHaltProps = {
  code?: "SH-08";
  reason?: SecurityHaltCode;
};

export function SecurityHalt({ code = "SH-08", reason }: SecurityHaltProps) {
  return (
    <section aria-label="Security Halt" role="alert" data-testid="security-halt">
      <h1>Security Halt</h1>
      <p>{code}</p>
      <p>Resolved surface context failed validation. Rendering stopped.</p>
      <p>No case evidence is rendered in this state.</p>
      {reason ? <p aria-label="Security halt reason">{reason}</p> : null}
    </section>
  );
}
