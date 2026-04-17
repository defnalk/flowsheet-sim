/** TypeScript interfaces matching the backend Pydantic models. */

export type UnitOpType = "flash" | "mccabe-thiele" | "reactor";

export interface SolverStatus {
  converged: boolean;
  iterations?: number;
  message?: string;
}

export interface ComponentSpec {
  name: string;
  molecular_weight: number;
  normal_boiling_point_k?: number;
  critical_temperature_k?: number;
  critical_pressure_pa?: number;
  acentric_factor?: number;
}

// Flash drum
export interface FlashDrumRequest {
  components: string[];
  feed_mole_fractions: number[];
  temperature_k: number;
  pressure_pa: number;
}

export interface FlashDrumResponse {
  vapour_fraction: number;
  liquid_fraction: number;
  liquid_composition: Record<string, number>;
  vapour_composition: Record<string, number>;
  k_values: Record<string, number>;
  temperature_k: number;
  pressure_pa: number;
  status: SolverStatus;
}

// McCabe-Thiele
export interface McCabeThieleRequest {
  alpha: number;
  x_D: number;
  x_B: number;
  x_F: number;
  q: number;
  R: number;
  max_stages?: number;
}

export interface McCabeThieleResponse {
  n_stages: number;
  feed_stage: number;
  x_stages: number[];
  y_stages: number[];
  diagram_base64: string;
  status: SolverStatus;
}

// Reactor
export interface ReactorRequest {
  reactor_type: "pfr" | "cstr" | "batch";
  rate_law_template: string;
  rate_law_params: Record<string, number>;
  species_names: string[];
  initial_concentrations: number[];
  volume_or_time_span: [number, number];
  flow_rate?: number;
  reactor_volume?: number;
  n_points?: number;
  key_species?: number;
}

export interface ReactorResponse {
  independent_variable: number[];
  concentrations: Record<string, number[]>;
  conversion: number[] | null;
  status: SolverStatus;
}

export type SolveResponse =
  | FlashDrumResponse
  | McCabeThieleResponse
  | ReactorResponse;
