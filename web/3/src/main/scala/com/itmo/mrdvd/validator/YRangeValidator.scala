package com.itmo.mrdvd.validator

import jakarta.faces.validator.FacesValidator

@FacesValidator
class YRangeValidator extends InRangeValidator(-2, 2)