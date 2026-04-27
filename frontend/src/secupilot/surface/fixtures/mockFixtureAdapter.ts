import type { ResolvedSurfaceContext } from "../context/types";
import { validateResolvedSurfaceContext } from "../context/validateResolvedSurfaceContext";
import { cloneFixtureContext, getFixtureRegistryEntry, listFixtureIds } from "./fixtureRegistry";
import type { FixtureKind, FixtureLoadOptions, MockFixtureAdapter } from "./fixtureTypes";

const VALIDATE_FALSE_LIMIT =
  "validate=false is only allowed when testing poison pill rejection behavior";

export function getMockFixture(id: string, options: FixtureLoadOptions = {}): ResolvedSurfaceContext {
  const registryEntry = getFixtureRegistryEntry(id);
  const shouldValidate = options.validate ?? true;

  if (!shouldValidate && registryEntry.kind !== "poison_pill") {
    throw new Error(`${VALIDATE_FALSE_LIMIT}: ${id}`);
  }

  const context = cloneFixtureContext(registryEntry.context);

  if (!shouldValidate) {
    return context as ResolvedSurfaceContext;
  }

  const result = validateResolvedSurfaceContext(context);
  if (!result.ok) {
    throw new Error(
      `Mock fixture ${id} failed validation with ${result.code}: ${result.reason}`
    );
  }

  return result.context;
}

export function createMockFixtureAdapter(): MockFixtureAdapter {
  return {
    getFixture: getMockFixture,
    listFixtureIds,
    listPhaseFixtures: () => listFixtureIds("phase"),
    listBoundaryFixtures: () => listFixtureIds("boundary_case"),
    listPoisonPillFixtures: () => listFixtureIds("poison_pill"),
    listResolverDegradationFixtures: () => listFixtureIds("resolver_degradation")
  };
}

export const mockFixtureAdapter = createMockFixtureAdapter();
