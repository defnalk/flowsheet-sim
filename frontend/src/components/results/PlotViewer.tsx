"use client";

import type { McCabeThieleResponse } from "@/lib/types";

interface PlotViewerProps {
  data: McCabeThieleResponse;
}

export default function PlotViewer({ data }: PlotViewerProps) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="rounded-lg border p-3">
          <p className="text-muted-foreground">Theoretical stages</p>
          <p className="text-2xl font-bold">{data.n_stages}</p>
        </div>
        <div className="rounded-lg border p-3">
          <p className="text-muted-foreground">Feed stage</p>
          <p className="text-2xl font-bold">{data.feed_stage}</p>
        </div>
      </div>

      <div className="rounded-lg border overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`data:image/png;base64,${data.diagram_base64}`}
          alt="McCabe-Thiele diagram"
          className="w-full"
        />
      </div>
    </div>
  );
}
