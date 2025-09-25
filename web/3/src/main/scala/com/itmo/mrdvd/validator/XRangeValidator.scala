package com.itmo.mrdvd.validator

import jakarta.faces.validator.FacesValidator

@FacesValidator
class XRangeValidator extends InRangeValidator(-3, 5)