package com.itmo.mrdvd.repository

trait CachingPagedRepository[In, Out, Id] extends PagedRepository[In, Out, Id]:
  def setCache(map: Array[Out]): Unit
