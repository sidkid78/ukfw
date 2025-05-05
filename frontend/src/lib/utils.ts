// Utility functions for formatting, parsing, etc.

export function formatConfidence(conf: number | undefined): string {
  if (conf === undefined) return 'N/A';
  return `${(conf * 100).toFixed(1)}%`;
}

export function truncate(str: string, max: number = 40): string {
  return str.length > max ? str.slice(0, max - 3) + '...' : str;
}
