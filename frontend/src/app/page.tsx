"use client";

import UnitOpPalette from "@/components/sidebar/UnitOpPalette";
import FlashDrumForm from "@/components/forms/FlashDrumForm";
import McCabeThieleForm from "@/components/forms/McCabeThieleForm";
import ReactorForm from "@/components/forms/ReactorForm";
import ResultsSummary from "@/components/results/ResultsSummary";
import { useSimStore } from "@/stores/useSimStore";

function ActiveForm() {
  const { selectedUnitOp } = useSimStore();

  switch (selectedUnitOp) {
    case "flash":
      return <FlashDrumForm />;
    case "mccabe-thiele":
      return <McCabeThieleForm />;
    case "reactor":
      return <ReactorForm />;
    default:
      return (
        <div className="flex items-center justify-center h-full text-muted-foreground">
          <p>Select a unit operation from the sidebar to begin</p>
        </div>
      );
  }
}

export default function Home() {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <UnitOpPalette />

      {/* Center — form */}
      <main className="flex-1 overflow-y-auto p-6 border-r">
        <div className="max-w-lg mx-auto">
          <ActiveForm />
        </div>
      </main>

      {/* Right — results */}
      <section className="w-[480px] shrink-0 overflow-y-auto p-6">
        <h2 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground mb-4">
          Results
        </h2>
        <ResultsSummary />
      </section>
    </div>
  );
}
