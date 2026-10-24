import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import HomeContent from "@/components/HomeContent";

describe("HomeContent", () => {
  it("shows an online status when the API is reachable", () => {
    render(<HomeContent apiOnline={true} apiBaseUrl="http://localhost:8010" />);

    expect(screen.getByText("online")).toBeInTheDocument();
    expect(screen.getByTestId("status-dot")).toHaveClass("bg-[var(--status-good)]");
    expect(screen.queryByText(/uvicorn/)).not.toBeInTheDocument();
  });

  it("shows an unreachable status and the start-the-API hint when the API is down", () => {
    render(<HomeContent apiOnline={false} apiBaseUrl="http://localhost:8010" />);

    expect(screen.getByText("unreachable")).toBeInTheDocument();
    expect(screen.getByTestId("status-dot")).toHaveClass("bg-[var(--status-bad)]");
    expect(screen.getByText(/uvicorn/)).toBeInTheDocument();
  });

  it("renders the given API base URL", () => {
    render(<HomeContent apiOnline={true} apiBaseUrl="http://example.test:9999" />);
    expect(screen.getByText(/example\.test:9999/)).toBeInTheDocument();
  });
});
