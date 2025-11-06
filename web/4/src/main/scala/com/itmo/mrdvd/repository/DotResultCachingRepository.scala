package com.itmo.mrdvd.repository

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Success, Failure}

class DotResultCachingRepository
    extends CachingRepository[DotResult, DotResult]:
  protected var genericRepository: GenericRepository[DotResult, DotResult] =
    null
  private var cache: Array[DotResult] = Array()

  protected def init: Unit =
    setCache(genericRepository.getAll)
  override def getAll: Array[DotResult] = cache
  override def create(item: DotResult): Try[DotResult] =
    genericRepository.create(item) match
      case Success(value) =>
        cache = value +: cache
        Success(value)
      case Failure(exception) =>
        Failure(exception)
  override def setCache(newCache: Array[DotResult]): Unit = cache = newCache
  override def clearAll: Unit =
    genericRepository.clearAll
    cache = Array()
