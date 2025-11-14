package com.itmo.mrdvd.repository.dot

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Success, Failure}
import com.itmo.mrdvd.repository._

class DotResultCachingRepository(
    private val groupedRepository: GroupedRepository[DotResult, DotResult, Int]
) extends CachingGroupRepository[DotResult, DotResult, Int]:
  private var cache = Map.empty[Int, Array[DotResult]]

  Try(groupedRepository.getAll) match
    case Success(newCache)  => setCache(newCache)
    case Failure(exception) =>
  override def getAll: Map[Int, Array[DotResult]] = cache
  override def create(id: Int, item: DotResult): Try[DotResult] =
    groupedRepository
      .create(id, item)
      .map(value =>
        val cachedGroup = cache.getOrElse(id, Array.empty[DotResult])
        cache = cache.updated(id, value +: cachedGroup)
        value
      )
  override def setCache(newCache: Map[Int, Array[DotResult]]): Unit = cache =
    newCache
  override def clearGroup(id: Int): Unit =
    groupedRepository.clearGroup(id)
    cache += (id -> Array())
  override def getGroup(id: Int): Try[Array[DotResult]] =
    Try(cache.get(id).get)
