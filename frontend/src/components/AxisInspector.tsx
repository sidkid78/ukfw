'use client';

import React from 'react';
import { AxisCoordinate } from '../lib/types';

// Define a type for the possible values within AxisCoordinate
type AxisValue = string | number | string[] | undefined | { [key: string]: string | string[] };

export default function AxisInspector({ axes = {} as AxisCoordinate, onAxisSelect }: { axes?: AxisCoordinate; onAxisSelect?: (axis: string, value: AxisValue) => void }) {
  return (
    <div className="space-y-1">
      {Object.entries(axes).map(([axis, value]) => (
        <div key={axis}>
          <strong>{axis.toUpperCase()}</strong>:&nbsp;
          <span
            className="underline cursor-pointer text-blue-600"
            onClick={() => onAxisSelect?.(axis, value)}
          >
            {String(value)}
          </span>
        </div>
      ))}
    </div>
  );
}
