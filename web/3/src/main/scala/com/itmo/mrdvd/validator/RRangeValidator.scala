package com.itmo.mrdvd.validator

import jakarta.faces.validator.FacesValidator

@FacesValidator("rRangeValidator")
class RRangeValidator extends InRangeValidator(1, 3)
