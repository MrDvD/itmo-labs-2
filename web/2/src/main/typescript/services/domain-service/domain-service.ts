export interface DotDomainService {
  getDotDomain(): string;
}

export class LabDotDomainService {
  public getDotDomain(): string {
    return "http://192.168.10.80:8529/";
  }
}
