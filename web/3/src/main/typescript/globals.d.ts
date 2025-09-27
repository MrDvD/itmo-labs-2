export {};

declare global {
  interface Window {
    sendPlot: () => void;
  }
}
