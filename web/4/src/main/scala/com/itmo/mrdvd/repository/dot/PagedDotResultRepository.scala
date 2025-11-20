package com.itmo.mrdvd.repository.dot

import com.itmo.mrdvd.repository._
import com.itmo.mrdvd.dto._
import scala.util.Try
import scala.util.Success
import scala.util.Failure

class PagedDotResultRepository(
    private val genericRepository: GroupedRepository[
      DotResult,
      Entry[Entry[Int, String], DotResult],
      Int
    ]
) extends CachingPagedRepository[
      Entry[Int, DotResult],
      Entry[Entry[Int, String], DotResult],
      Int
    ]:
  private var cache = genericRepository.getAll.toArray
  override def getAll: Iterator[Entry[Entry[Int, String], DotResult]] =
    cache.iterator
  override def create(
      item: Entry[Int, DotResult]
  ): Try[Entry[Entry[Int, String], DotResult]] =
    genericRepository
      .create(item.key, item.value)
      .map(value =>
        cache :+ value
        value
      )
  override def setCache(
      newCache: Array[Entry[Entry[Int, String], DotResult]]
  ): Unit = cache = newCache
  override def getPage(
      page: Int,
      pageSize: Int
  ): Try[Page[Entry[Entry[Int, String], DotResult]]] =
    val totalPages = Math.ceil(cache.length.toDouble / pageSize).toInt
    if page < 0 || page > totalPages then Failure(Error("Page does not exist"))
    val currentPageIdx = page * pageSize
    val pages = cache.slice(currentPageIdx, currentPageIdx + pageSize)
    Success(
      Page(
        items = pages.toList,
        pageNumber = page,
        pageSize = pageSize,
        totalItems = cache.length,
        totalPages = totalPages
      )
    )
  override def remove(userId: Int): Unit =
    genericRepository.clearGroup(userId)
