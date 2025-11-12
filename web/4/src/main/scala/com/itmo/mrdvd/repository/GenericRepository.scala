package com.itmo.mrdvd.repository

import scala.util.Try

trait GenericRepository[In, Out, Id]:
  def create(obj: In): Try[Out]
  def get(id: Id): Try[Out]
  def remove(id: Id): Unit
