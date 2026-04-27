import type { ResolvedSurfaceContext } from "../context/types";

export type FixtureKind =
  | "phase"
  | "boundary_case"
  | "poison_pill"
  | "resolver_degradation";

export type FixtureExpectedValidation = "pass" | "fail_closed";

export interface FixtureLoadOptions {
  // validate=false is ONLY allowed when testing poison pill rejection behavior.
  // All production-like, Storybook, and Playwright fixture usage must use validate=true.
  // Never set validate=false to work around context issues in page rendering.
  validate?: boolean;
}

export interface FixtureRegistryEntry {
  id: string;
  kind: FixtureKind;
  description: string;
  expectedValidation: FixtureExpectedValidation;
  // Poison-pill entries intentionally use the wider shape so rejection tests can
  // feed malformed payloads into ContextValidator without weakening renderable fixtures.
  context: ResolvedSurfaceContext | Record<string, unknown>;
}

export interface MockFixtureAdapter {
  getFixture(id: string, options?: FixtureLoadOptions): ResolvedSurfaceContext;
  listFixtureIds(kind?: FixtureKind): string[];
  listPhaseFixtures(): string[];
  listBoundaryFixtures(): string[];
  listPoisonPillFixtures(): string[];
  listResolverDegradationFixtures(): string[];
}
