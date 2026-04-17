"use client";

import { useSimStore } from "@/stores/useSimStore";
import type {
  FlashDrumResponse,
  McCabeThieleResponse,
  ReactorResponse,
} from "@/lib/types";
import StreamTable from "./StreamTable";
import PlotViewer from "./PlotViewer";
import ReactorPlot from "./ReactorPlot";

function isFlashResponse(r: unknown): r is FlashDrumResponse {
  return typeof r === "object" && r !== null && "vapour_fraction" in r;
}

function isMcCabeResponse(r: unknown): r is McCabeThieleResponse {
  return typeof r === "object" && r !== null && "diagram_base64" in r;
}

function isReactorResponse(r: unknown): r is ReactorResponse {
  return typeof r === "object" && r !== null && "concentrations" in r && "independent_variable" in r;
}

export default function ResultsSummary() {
  const { results, error, isLoading, selectedUnitOp } = useSimStore();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-center space-y-2">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
          <p>Solving...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
        <p className="font-medium">Error</p>
        <p className="text-sm mt-1">{error}</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <p className="text-center">
          {selectedUnitOp
            ? "Configure parameters and click Solve"
            : "Select a unit operation from the sidebar"}
        </p>
      </div>
    );
  }

  if (isFlashResponse(results)) return <StreamTable data={results} />;
  if (isMcCabeResponse(results)) return <PlotViewer data={results} />;
  if (isReactorResponse(results)) return <ReactorPlot data={results} />;

  return null;
}
