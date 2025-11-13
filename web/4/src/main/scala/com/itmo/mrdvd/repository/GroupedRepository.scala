package com.itmo.mrdvd.repository

import scala.util.Try

trait GroupedRepository[In, Out, GroupId]:
  def create(id: GroupId, obj: In): Try[Out]
  def getAll: Map[GroupId, Array[Out]]
  def getGroup(id: GroupId): Try[Array[Out]]
  def clearGroup(id: GroupId): Unit
