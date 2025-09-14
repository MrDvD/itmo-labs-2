export interface DotDomainService {
  getDotDomain(): string;
};

export class LabDotDomainService {
  public getDotDomain(): string {
    return "http://localhost:8080/";
  }
}