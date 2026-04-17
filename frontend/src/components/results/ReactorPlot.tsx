"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { ReactorResponse } from "@/lib/types";

interface ReactorPlotProps {
  data: ReactorResponse;
}

const COLORS = ["#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed", "#0891b2"];

export default function ReactorPlot({ data }: ReactorPlotProps) {
  const species = Object.keys(data.concentrations);
  const n = data.independent_variable.length;

  // Build chart data: [{x: ..., A: ..., B: ..., conversion: ...}, ...]
  const chartData = Array.from({ length: n }, (_, i) => {
    const point: Record<string, number> = {
      x: data.independent_variable[i],
    };
    for (const s of species) {
      point[s] = data.concentrations[s][i];
    }
    if (data.conversion) {
      point.conversion = data.conversion[i];
    }
    return point;
  });

  const isBatch = n > 1;
  const xLabel = isBatch ? "Volume or Time" : "Steady State";

  // Final values summary
  const finalIdx = n - 1;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-3 text-sm">
        {species.map((s) => (
          <div key={s} className="rounded-lg border p-3">
            <p className="text-muted-foreground">C_{s} (final)</p>
            <p className="text-lg font-bold">
              {data.concentrations[s][finalIdx].toFixed(4)} mol/m³
            </p>
          </div>
        ))}
        {data.conversion && (
          <div className="rounded-lg border p-3">
            <p className="text-muted-foreground">Conversion</p>
            <p className="text-lg font-bold">
              {(data.conversion[finalIdx] * 100).toFixed(1)}%
            </p>
          </div>
        )}
      </div>

      {n > 1 && (
        <div className="rounded-lg border p-4 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="x"
                label={{ value: xLabel, position: "insideBottom", offset: -5 }}
                tickFormatter={(v: number) => v.toFixed(1)}
              />
              <YAxis label={{ value: "Concentration (mol/m³)", angle: -90, position: "insideLeft" }} />
              <Tooltip formatter={(v) => typeof v === "number" ? v.toFixed(4) : v} />
              <Legend />
              {species.map((s, i) => (
                <Line
                  key={s}
                  type="monotone"
                  dataKey={s}
                  stroke={COLORS[i % COLORS.length]}
                  dot={false}
                  strokeWidth={2}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
