package com.itmo.mrdvd.repository.dot

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Success, Failure}
import com.itmo.mrdvd.repository.GroupedRepository
import com.itmo.mrdvd.repository.CachingGroupRepository

class DotResultCachingRepository(
    private val groupedRepository: GroupedRepository[DotResult, DotResult, Int]
) extends CachingGroupRepository[DotResult, DotResult, Int]:
  private var cache: Map[Int, Array[DotResult]] = Map()

  Try(groupedRepository.getAll) match
    case Success(newCache)  => setCache(newCache)
    case Failure(exception) =>
  override def getAll: Map[Int, Array[DotResult]] = cache
  override def create(id: Int, item: DotResult): Try[DotResult] =
    groupedRepository.create(id, item) match
      case Success(value) =>
        var possibleCachedGroup = cache.get(id)
        var cachedGroup: Array[DotResult] = null
        if possibleCachedGroup.isEmpty then cachedGroup = Array[DotResult]()
        else cachedGroup = possibleCachedGroup.get
        cachedGroup = value +: cachedGroup
        cache = cache + (id -> cachedGroup)
        Success(value)
      case Failure(exception) =>
        Failure(exception)
  override def setCache(newCache: Map[Int, Array[DotResult]]): Unit = cache =
    newCache
  override def clearGroup(id: Int): Unit =
    groupedRepository.clearGroup(id)
    cache += (id -> Array())
  override def getGroup(id: Int): Try[Array[DotResult]] =
    Try(cache.get(id).get)
