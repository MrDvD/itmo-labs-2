export interface DotDomainService {
  getDotDomain(): string;
};

export class LabDotDomainService {
  public getDotDomain(): string {
    return "https://lab-web.cloudpub.ru/graphql";
  }
}