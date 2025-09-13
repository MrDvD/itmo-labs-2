package com.itmo.mrdvd.validator

import com.itmo.mrdvd.dto.RawDot

class RawDotValidator extends Validator[RawDot] {
  override def validate(dot: RawDot): ValidationStatus = 
    val validationStatus = ValidationStatus(true)
    return validationStatus
}
