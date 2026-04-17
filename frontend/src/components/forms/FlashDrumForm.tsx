"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useSimStore } from "@/stores/useSimStore";
import { fetchComponents, solveFlash } from "@/lib/api";
import type { ComponentSpec } from "@/lib/types";

export default function FlashDrumForm() {
  const { setResults, setLoading, setError, isLoading } = useSimStore();

  const [availableComponents, setAvailableComponents] = useState<ComponentSpec[]>([]);
  const [comp1, setComp1] = useState("methanol");
  const [comp2, setComp2] = useState("water");
  const [z1, setZ1] = useState("0.5");
  const [temperature, setTemperature] = useState("340");
  const [pressure, setPressure] = useState("101325");

  useEffect(() => {
    fetchComponents()
      .then(setAvailableComponents)
      .catch(() => {});
  }, []);

  const handleSolve = async () => {
    const z1Val = parseFloat(z1);
    if (isNaN(z1Val) || z1Val < 0 || z1Val > 1) {
      setError("z₁ must be between 0 and 1");
      return;
    }

    setLoading(true);
    try {
      const result = await solveFlash({
        components: [comp1, comp2],
        feed_mole_fractions: [z1Val, 1 - z1Val],
        temperature_k: parseFloat(temperature),
        pressure_pa: parseFloat(pressure),
      });
      setResults(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Solve failed");
    }
  };

  // Filter for Antoine-supported components (those in the sepflows database)
  const compOptions = availableComponents.length > 0
    ? availableComponents
    : [{ name: "methanol" }, { name: "water" }, { name: "ethanol" }, { name: "dme" }];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Flash Drum</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="comp1">Component 1</Label>
            <select
              id="comp1"
              value={comp1}
              onChange={(e) => setComp1(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              {compOptions.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="comp2">Component 2</Label>
            <select
              id="comp2"
              value={comp2}
              onChange={(e) => setComp2(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              {compOptions.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="z1">z₁ (mole fraction of {comp1})</Label>
          <Input id="z1" type="number" step="0.01" min="0" max="1" value={z1} onChange={(e) => setZ1(e.target.value)} />
          <p className="text-xs text-muted-foreground">z₂ = {(1 - parseFloat(z1 || "0")).toFixed(4)}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="temp">Temperature (K)</Label>
            <Input id="temp" type="number" step="1" value={temperature} onChange={(e) => setTemperature(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="pres">Pressure (Pa)</Label>
            <Input id="pres" type="number" step="1000" value={pressure} onChange={(e) => setPressure(e.target.value)} />
          </div>
        </div>

        <Button onClick={handleSolve} disabled={isLoading} className="w-full">
          {isLoading ? "Solving..." : "Solve Flash"}
        </Button>
      </CardContent>
    </Card>
  );
}
