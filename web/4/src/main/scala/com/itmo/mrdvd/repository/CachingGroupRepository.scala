package com.itmo.mrdvd.repository

trait CachingGroupRepository[In, Out, GroupId]
    extends GroupedRepository[In, Out, GroupId]:
  def setCache(map: Map[GroupId, Array[Out]]): Unit
