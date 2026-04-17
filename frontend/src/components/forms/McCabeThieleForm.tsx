"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useSimStore } from "@/stores/useSimStore";
import { solveMcCabeThiele } from "@/lib/api";

export default function McCabeThieleForm() {
  const { setResults, setLoading, setError, isLoading } = useSimStore();

  const [alpha, setAlpha] = useState("2.5");
  const [xD, setXD] = useState("0.95");
  const [xB, setXB] = useState("0.05");
  const [xF, setXF] = useState("0.5");
  const [q, setQ] = useState("1.0");
  const [R, setR] = useState("1.5");

  const handleSolve = async () => {
    setLoading(true);
    try {
      const result = await solveMcCabeThiele({
        alpha: parseFloat(alpha),
        x_D: parseFloat(xD),
        x_B: parseFloat(xB),
        x_F: parseFloat(xF),
        q: parseFloat(q),
        R: parseFloat(R),
      });
      setResults(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Solve failed");
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>McCabe-Thiele Distillation</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="alpha">Relative volatility (alpha)</Label>
          <Input id="alpha" type="number" step="0.1" min="1.01" value={alpha} onChange={(e) => setAlpha(e.target.value)} />
        </div>

        <div className="grid grid-cols-3 gap-3">
          <div className="space-y-2">
            <Label htmlFor="xD">x_D (distillate)</Label>
            <Input id="xD" type="number" step="0.01" min="0" max="1" value={xD} onChange={(e) => setXD(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="xF">x_F (feed)</Label>
            <Input id="xF" type="number" step="0.01" min="0" max="1" value={xF} onChange={(e) => setXF(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="xB">x_B (bottoms)</Label>
            <Input id="xB" type="number" step="0.01" min="0" max="1" value={xB} onChange={(e) => setXB(e.target.value)} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="q">Feed quality (q)</Label>
            <Input id="q" type="number" step="0.1" value={q} onChange={(e) => setQ(e.target.value)} />
            <p className="text-xs text-muted-foreground">1 = sat. liquid, 0 = sat. vapor</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="R">Reflux ratio (L/D)</Label>
            <Input id="R" type="number" step="0.1" min="0.1" value={R} onChange={(e) => setR(e.target.value)} />
          </div>
        </div>

        <Button onClick={handleSolve} disabled={isLoading} className="w-full">
          {isLoading ? "Solving..." : "Solve McCabe-Thiele"}
        </Button>
      </CardContent>
    </Card>
  );
}
