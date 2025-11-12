package com.itmo.mrdvd.repository

trait CachingGroupRepository[In, Out, GroupId] extends GroupedRepository[In, Out, GroupId]:
  def setCache(array: Map[GroupId, Out]): Unit
