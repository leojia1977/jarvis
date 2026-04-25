import { ReactNode } from "react";
import { SecurityHalt } from "../components/SecurityHalt";
import { ResolvedSurfaceContext, SecurityHaltCode } from "./types";
import { validateResolvedSurfaceContext } from "./validateResolvedSurfaceContext";

type ResolvedSurfaceContextProviderProps = {
  input: unknown;
  children: (context: ResolvedSurfaceContext) => ReactNode;
  onInvalidContext?: (code: SecurityHaltCode, reason: string) => void;
};

export function ResolvedSurfaceContextProvider({
  input,
  children,
  onInvalidContext
}: ResolvedSurfaceContextProviderProps) {
  const result = validateResolvedSurfaceContext(input);

  if (!result.ok) {
    onInvalidContext?.(result.code, result.reason);
    return <SecurityHalt code="SH-08" reason={result.code} />;
  }

  return <>{children(result.context)}</>;
}
