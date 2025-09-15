export interface DotDomainService {
  getDotDomain(): string;
}

export class LabDotDomainService {
  public getDotDomain(): string {
    return "https://se.ifmo.ru:8529/~s466449/";
  }
}
