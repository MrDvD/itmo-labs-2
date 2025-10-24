export {};

declare global {
  interface Window {
    initialData: {
      currentPageComponent: any;
    };
  }
}