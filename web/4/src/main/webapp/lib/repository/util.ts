export interface Repository<_T, _C> {}

export interface ReactiveRepository<_T, _C, Cache> extends Repository<_T, _C> {
  getCache(): Cache;
}

export interface RepositoryBuilder<_T, _C, R extends Repository<_T, _C>> {
  build(): R
}