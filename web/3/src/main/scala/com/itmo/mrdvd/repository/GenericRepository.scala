package com.itmo.mrdvd.repository

import scala.util.Try

trait GenericRepository[T, U]:
  def create(item: T): Try[U]
  def getAll(): Array[U]
