package com.itmo.mrdvd.validator

import jakarta.faces.validator.FacesValidator

@FacesValidator("xRangeValidator")
class XRangeValidator extends InRangeValidator(-3, 5)