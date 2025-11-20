package com.itmo.mrdvd.repository

import scala.util.Try
import com.itmo.mrdvd.dto.Page

trait PagedRepository[In, Out, Id]:
  def create(obj: In): Try[Out]
  def getPage(page: Int, pageSize: Int): Try[Page[Out]]
  def getAll: Iterator[Out]
  def remove(id: Id): Unit
