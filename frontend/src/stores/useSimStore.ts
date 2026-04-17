/** Zustand store for the single-unit-op simulator. */

import { create } from "zustand";
import type {
  UnitOpType,
  SolveResponse,
} from "@/lib/types";

interface SimState {
  selectedUnitOp: UnitOpType | null;
  results: SolveResponse | null;
  isLoading: boolean;
  error: string | null;
  setUnitOp: (op: UnitOpType) => void;
  setResults: (r: SolveResponse) => void;
  setLoading: (v: boolean) => void;
  setError: (e: string | null) => void;
  clearResults: () => void;
}

export const useSimStore = create<SimState>((set) => ({
  selectedUnitOp: null,
  results: null,
  isLoading: false,
  error: null,
  setUnitOp: (op) => set({ selectedUnitOp: op, results: null, error: null }),
  setResults: (r) => set({ results: r, isLoading: false, error: null }),
  setLoading: (v) => set({ isLoading: v }),
  setError: (e) => set({ error: e, isLoading: false }),
  clearResults: () => set({ results: null, error: null }),
}));
