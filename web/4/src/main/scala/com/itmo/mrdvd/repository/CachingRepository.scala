package com.itmo.mrdvd.repository

trait CachingRepository[In, Out, Id] extends GenericRepository[In, Out, Id]:
  def setCache(map: Map[Id, Out]): Unit
