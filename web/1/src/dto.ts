export type DotParams = {
  X: string;
  Y: number;
  R: string;
}

export type DotStatus = {
  entry: DotParams;
  hit: boolean;
};

export function isDotParams(object: unknown): object is DotParams {
  return object instanceof Object &&
    'X' in object && typeof object['X'] === 'string' &&
    'Y' in object && typeof object['Y'] === 'number' &&
    'R' in object && typeof object['R'] === 'string';
}

export function isDotStatus(object: unknown): object is DotStatus {
  return object instanceof Object &&
    'entry' in object && isDotParams(object['entry']);
}