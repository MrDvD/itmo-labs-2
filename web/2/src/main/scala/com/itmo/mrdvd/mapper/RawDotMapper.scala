package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.validator.Validator

class RawDotMapper(rawDotValidator: Validator[RawDot]) extends Mapper[RawDot, Dot](rawDotValidator):
  override def map(rawDot: RawDot): Option[Dot] =
    val validationResult = rawDotValidator.validate(rawDot)
    if !validationResult.valid then
      return Option.empty[Dot]
    val dot = Dot(rawDot.X.toInt, rawDot.Y.toFloat, rawDot.R.toFloat)
    return Option[Dot](dot)
