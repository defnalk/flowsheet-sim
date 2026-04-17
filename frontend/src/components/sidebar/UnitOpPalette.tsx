"use client";

import { useSimStore } from "@/stores/useSimStore";
import type { UnitOpType } from "@/lib/types";
import { cn } from "@/lib/utils";

const UNIT_OPS: { id: UnitOpType; label: string; icon: string; desc: string }[] = [
  {
    id: "flash",
    label: "Flash Drum",
    icon: "⚗️",
    desc: "Isothermal VLE flash separation",
  },
  {
    id: "mccabe-thiele",
    label: "McCabe-Thiele",
    icon: "📐",
    desc: "Binary distillation staging diagram",
  },
  {
    id: "reactor",
    label: "Reactor (PFR)",
    icon: "🔬",
    desc: "Plug flow / CSTR / batch kinetics",
  },
];

export default function UnitOpPalette() {
  const { selectedUnitOp, setUnitOp } = useSimStore();

  return (
    <aside className="w-60 shrink-0 border-r bg-muted/40 p-4 space-y-2 overflow-y-auto">
      <h2 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground mb-3">
        Unit Operations
      </h2>
      {UNIT_OPS.map((op) => (
        <button
          key={op.id}
          onClick={() => setUnitOp(op.id)}
          className={cn(
            "w-full text-left rounded-lg border p-3 transition-colors hover:bg-accent",
            selectedUnitOp === op.id && "border-primary bg-accent",
          )}
        >
          <div className="flex items-center gap-2">
            <span className="text-xl">{op.icon}</span>
            <span className="font-medium text-sm">{op.label}</span>
          </div>
          <p className="text-xs text-muted-foreground mt-1">{op.desc}</p>
        </button>
      ))}
    </aside>
  );
}
