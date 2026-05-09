import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { EciChainIndicator } from "./EciChainIndicator";
import { VfeForecastCard } from "./VfeForecastCard";
import { buildEciChainIndicatorView, buildVfeForecastCardView } from "./eciVfeUiModel";

describe("ECI/VFE chain indicator ui model", () => {
  it("loads guard-passed cards with evidence-gap guidance", () => {
    const cards = buildEciChainIndicatorView();
    expect(cards.length).toBeGreaterThan(0);

    for (const card of cards) {
      expect(card.confidence).toBeGreaterThanOrEqual(0);
      expect(card.confidence).toBeLessThanOrEqual(1);
      expect(card.evidenceGapCount).toBeGreaterThan(0);
      for (const gap of card.evidenceGaps) {
        expect(gap.urgency.length).toBeGreaterThan(0);
        expect(gap.windowClosesIn.length).toBeGreaterThan(0);
        expect(gap.fallbackIfMissed.length).toBeGreaterThan(0);
      }
    }
  });

  it("renders case cards without raw evidence fields", () => {
    render(<EciChainIndicator />);

    const surface = screen.getByTestId("eci-chain-indicator-view");
    expect(surface).toHaveAttribute("data-output-guard-status", "PASS");
    expect(surface).toHaveAttribute("data-real-data", "false");
    expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    expect(surface).toHaveAttribute("data-production-writeback", "false");

    const cards = screen.getAllByTestId("eci-chain-indicator-card");
    expect(cards.length).toBeGreaterThanOrEqual(6);

    const text = surface.textContent ?? "";
    expect(text).not.toMatch(/raw payload|raw evidence|authorization|bearer|api_key/i);
  });
});

describe("ECI/VFE forecast card ui model", () => {
  it("loads guard-passed forecast cards with evidence-gap guidance", () => {
    const cards = buildVfeForecastCardView();
    expect(cards.length).toBeGreaterThan(0);

    for (const card of cards) {
      expect(card.confidence).toBeGreaterThanOrEqual(0);
      expect(card.confidence).toBeLessThanOrEqual(1);
      expect(card.attackPathDefensiveSummary.length).toBeGreaterThan(0);
      expect(card.evidenceGaps.length).toBeGreaterThan(0);
      for (const gap of card.evidenceGaps) {
        expect(gap.urgency.length).toBeGreaterThan(0);
        expect(gap.windowClosesIn.length).toBeGreaterThan(0);
        expect(gap.deadlineBasis.length).toBeGreaterThan(0);
        expect(gap.fallbackIfMissed.length).toBeGreaterThan(0);
      }
    }
  });

  it("renders defensive forecast cards without attacker-readable text", () => {
    render(<VfeForecastCard />);

    const surface = screen.getByTestId("vfe-forecast-card-view");
    expect(surface).toHaveAttribute("data-output-guard-status", "PASS");
    expect(surface).toHaveAttribute("data-real-data", "false");
    expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    expect(surface).toHaveAttribute("data-production-writeback", "false");

    const cards = screen.getAllByTestId("vfe-forecast-card");
    expect(cards.length).toBeGreaterThanOrEqual(5);

    const text = surface.textContent ?? "";
    expect(text).toMatch(/Defensive summary/i);
    expect(text).toMatch(/Collection window:/i);
    expect(text).toMatch(/Deadline basis:/i);
    expect(text).not.toMatch(/attack_path|exploit|payload|poc|authorization|bearer|topology/i);
  });
});
