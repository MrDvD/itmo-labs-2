package com.itmo.mrdvd.repository

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Success, Failure}
import jakarta.inject.{Named, Inject}
import jakarta.enterprise.context.ApplicationScoped
import jakarta.annotation.PostConstruct

@Named("cachingRepository")
@ApplicationScoped
class DotResultCachingRepository extends CachingRepository[DotResult, DotResult]:
  @Inject @Named("jdbcRepository") private var genericRepository: GenericRepository[DotResult, DotResult] = null
  private var cache: Array[DotResult] = Array()

  @PostConstruct
  private def init(): Unit =
    setCache(genericRepository.getAll())
  override def getAll(): Array[DotResult] = cache
  override def create(item: DotResult): Try[DotResult] =
    genericRepository.create(item) match
      case Success(value) =>
        cache +:= value
        Success(value)
      case Failure(exception) =>
        Failure(exception)
  override def setCache(newCache: Array[DotResult]): Unit = cache = newCache