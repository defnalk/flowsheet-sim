"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useSimStore } from "@/stores/useSimStore";
import { solveReactor } from "@/lib/api";

const TEMPLATES = [
  { value: "first_order", label: "First order: A → B" },
  { value: "second_order", label: "Second order: A → B" },
  { value: "reversible_first_order", label: "Reversible: A ⇌ B" },
  { value: "michaelis_menten", label: "Michaelis-Menten: S → P" },
];

export default function ReactorForm() {
  const { setResults, setLoading, setError, isLoading } = useSimStore();

  const [reactorType, setReactorType] = useState<"pfr" | "cstr" | "batch">("pfr");
  const [template, setTemplate] = useState("first_order");
  const [k, setK] = useState("0.1");
  const [c0, setC0] = useState("1.0");
  const [spanEnd, setSpanEnd] = useState("10");
  const [flowRate, setFlowRate] = useState("0.01");
  const [reactorVol, setReactorVol] = useState("10");

  const handleSolve = async () => {
    setLoading(true);

    const params: Record<string, number> = {};
    if (template === "reversible_first_order") {
      params.kf = parseFloat(k);
      params.kr = parseFloat(k) * 0.5;
    } else if (template === "michaelis_menten") {
      params.Vmax = parseFloat(k);
      params.Km = 0.5;
    } else {
      params.k = parseFloat(k);
    }

    try {
      const result = await solveReactor({
        reactor_type: reactorType,
        rate_law_template: template,
        rate_law_params: params,
        species_names: ["A", "B"],
        initial_concentrations: [parseFloat(c0), 0.0],
        volume_or_time_span: [0, parseFloat(spanEnd)],
        flow_rate: reactorType !== "batch" ? parseFloat(flowRate) : undefined,
        reactor_volume: reactorType === "cstr" ? parseFloat(reactorVol) : undefined,
        n_points: 200,
        key_species: 0,
      });
      setResults(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Solve failed");
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Reactor Simulation</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label>Reactor type</Label>
          <div className="flex gap-2">
            {(["pfr", "cstr", "batch"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setReactorType(t)}
                className={`px-3 py-1.5 rounded-md border text-sm font-medium transition-colors ${
                  reactorType === t
                    ? "bg-primary text-primary-foreground"
                    : "bg-background hover:bg-accent"
                }`}
              >
                {t.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="template">Rate law</Label>
          <select
            id="template"
            value={template}
            onChange={(e) => setTemplate(e.target.value)}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            {TEMPLATES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="k">Rate constant (k)</Label>
            <Input id="k" type="number" step="0.01" value={k} onChange={(e) => setK(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="c0">C_A0 (mol/m³)</Label>
            <Input id="c0" type="number" step="0.1" min="0" value={c0} onChange={(e) => setC0(e.target.value)} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="span">
              {reactorType === "batch" ? "Time end (s)" : "Volume end (m³)"}
            </Label>
            <Input id="span" type="number" step="1" value={spanEnd} onChange={(e) => setSpanEnd(e.target.value)} />
          </div>
          {reactorType !== "batch" && (
            <div className="space-y-2">
              <Label htmlFor="flow">Flow rate Q (m³/s)</Label>
              <Input id="flow" type="number" step="0.001" value={flowRate} onChange={(e) => setFlowRate(e.target.value)} />
            </div>
          )}
        </div>

        {reactorType === "cstr" && (
          <div className="space-y-2">
            <Label htmlFor="vol">Reactor volume (m³)</Label>
            <Input id="vol" type="number" step="1" value={reactorVol} onChange={(e) => setReactorVol(e.target.value)} />
          </div>
        )}

        <Button onClick={handleSolve} disabled={isLoading} className="w-full">
          {isLoading ? "Solving..." : `Solve ${reactorType.toUpperCase()}`}
        </Button>
      </CardContent>
    </Card>
  );
}
