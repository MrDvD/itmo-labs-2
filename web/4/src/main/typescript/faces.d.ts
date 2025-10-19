declare const faces: {
  ajax: {
    request(
      source: Element,
      event: Event,
      options: {
        execute?: string;
        render?: string;
        [key: string]: any;
      },
    ): void;
  };
};
