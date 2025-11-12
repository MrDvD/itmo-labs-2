package com.itmo.mrdvd.repository

import scala.util.Try

trait GroupedRepository[In, Out, GroupId]:
  def create(id: GroupId, obj: In): Try[Out] 
  def getAll: Map[GroupId, Array[Out]]
  def clearAll: Unit
  def getGroup(id: GroupId): Try[Out]
  def clearGroup(id: GroupId): Unit
