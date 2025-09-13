package com.itmo.mrdvd.validator

trait Validator[T] {
  def validate(obj: T): ValidationStatus
}
