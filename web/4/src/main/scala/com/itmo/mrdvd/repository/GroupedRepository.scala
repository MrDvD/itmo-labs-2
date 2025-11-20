package com.itmo.mrdvd.repository

import scala.util.Try

trait GroupedRepository[In, Out, GroupId]:
  def create(id: GroupId, obj: In): Try[Out]
  def getAll: Iterator[Out]
  def getGroup(id: GroupId): Iterator[Try[Out]]
  def clearGroup(id: GroupId): Unit
