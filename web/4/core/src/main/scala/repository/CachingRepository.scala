package com.itmo.mrdvd.repository

trait CachingRepository[T, U] extends GenericRepository[T, U]:
  def setCache(array: Array[U]): Unit
