export interface Repository<_T, _C> {}

export interface ReactiveRepository<_T, _C> extends Repository<_T, _C> {
  getCache(): _T[];
}

export interface RepositoryBuilder<_T, _C, R extends Repository<_T, _C>> {
  build(): R
}