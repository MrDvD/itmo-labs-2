package com.itmo.mrdvd.validator

import jakarta.faces.validator.FacesValidator

@FacesValidator("yRangeValidator")
class YRangeValidator extends InRangeValidator(-2, 2)