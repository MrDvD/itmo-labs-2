export interface DotDomainService {
  getDotDomain(): string;
};

export class LabDotDomainService {
  public getDotDomain(): string {
    return window.location.origin + "/dot-params";
  }
}