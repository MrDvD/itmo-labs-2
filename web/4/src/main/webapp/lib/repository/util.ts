export interface Repository<_T, _C> {}

export interface RepositoryBuilder<_T, _C, R extends Repository<_T, _C>> {
  build(): R
}