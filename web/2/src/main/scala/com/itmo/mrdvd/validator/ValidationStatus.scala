package com.itmo.mrdvd.validator

class ValidationStatus(val valid: Boolean, val errors: Array[ValidationError] = Array[ValidationError]())
