"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { FlashDrumResponse } from "@/lib/types";

interface StreamTableProps {
  data: FlashDrumResponse;
}

export default function StreamTable({ data }: StreamTableProps) {
  const components = Object.keys(data.liquid_composition);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="rounded-lg border p-3">
          <p className="text-muted-foreground">Vapour fraction</p>
          <p className="text-2xl font-bold">{data.vapour_fraction.toFixed(4)}</p>
        </div>
        <div className="rounded-lg border p-3">
          <p className="text-muted-foreground">Liquid fraction</p>
          <p className="text-2xl font-bold">{data.liquid_fraction.toFixed(4)}</p>
        </div>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Component</TableHead>
            <TableHead className="text-right">Feed (z)</TableHead>
            <TableHead className="text-right">Liquid (x)</TableHead>
            <TableHead className="text-right">Vapour (y)</TableHead>
            <TableHead className="text-right">K-value</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {components.map((comp) => (
            <TableRow key={comp}>
              <TableCell className="font-medium">{comp}</TableCell>
              <TableCell className="text-right">
                {(
                  data.liquid_composition[comp] * data.liquid_fraction +
                  data.vapour_composition[comp] * data.vapour_fraction
                ).toFixed(4)}
              </TableCell>
              <TableCell className="text-right">
                {data.liquid_composition[comp].toFixed(4)}
              </TableCell>
              <TableCell className="text-right">
                {data.vapour_composition[comp].toFixed(4)}
              </TableCell>
              <TableCell className="text-right">
                {data.k_values[comp].toFixed(4)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
