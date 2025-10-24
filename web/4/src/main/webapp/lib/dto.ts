export type DotParams = {
  X: number;
  Y: number;
  R: number;
}

export type DotStatus = {
  entry: DotParams;
  hit: boolean;
  date: string;
};

export function isDotParams(object: unknown): object is DotParams {
  return object instanceof Object &&
    'X' in object && typeof object['X'] === 'number' &&
    'Y' in object && typeof object['Y'] === 'number' &&
    'R' in object && typeof object['R'] === 'number';
}

export function isDotStatus(object: unknown): object is DotStatus {
  return object instanceof Object &&
    'entry' in object && isDotParams(object['entry']);
}