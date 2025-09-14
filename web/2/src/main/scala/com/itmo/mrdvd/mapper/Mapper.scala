package com.itmo.mrdvd.mapper

trait Mapper[T, U]:
  def map(obj: T): Option[U]