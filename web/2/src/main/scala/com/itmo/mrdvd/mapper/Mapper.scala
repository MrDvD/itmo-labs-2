package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.validator.Validator

abstract class Mapper[T, U](validator: Validator[T]):
  def map(obj: T): Option[U]