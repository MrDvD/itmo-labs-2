package com.itmo.mrdvd.repository.dot

import com.itmo.mrdvd.dto._
import scala.util.{Try, Success, Failure}
import com.itmo.mrdvd.repository._

class DotResultCachingRepository(
    private val groupedRepository: GroupedRepository[
      DotResult,
      Entry[String, DotResult],
      Int
    ]
) extends CachingGroupRepository[DotResult, Entry[String, DotResult], Int]:
  private var cache = groupedRepository.getAll
  override def getAll: Map[Int, Array[Entry[String, DotResult]]] = cache
  override def create(id: Int, item: DotResult): Try[Entry[String, DotResult]] =
    groupedRepository
      .create(id, item)
      .map(value =>
        val cachedGroup =
          cache.getOrElse(id, Array.empty[Entry[String, DotResult]])
        setCache(cache.updated(id, value +: cachedGroup))
        value
      )
  override def setCache(
      newCache: Map[Int, Array[Entry[String, DotResult]]]
  ): Unit = cache = newCache
  override def clearGroup(id: Int): Unit =
    groupedRepository.clearGroup(id)
    cache += (id -> Array())
  override def getGroup(id: Int): Try[Array[Entry[String, DotResult]]] =
    Try(cache.getOrElse(id, Array.empty[Entry[String, DotResult]]))
