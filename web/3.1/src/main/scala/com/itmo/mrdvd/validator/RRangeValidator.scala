package com.itmo.mrdvd.validator

import jakarta.faces.validator.FacesValidator

@FacesValidator
class RRangeValidator extends InRangeValidator(1, 3)
