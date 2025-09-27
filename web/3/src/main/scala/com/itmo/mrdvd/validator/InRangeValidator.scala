package com.itmo.mrdvd.validator

import jakarta.faces.validator.{Validator, ValidatorException}
import jakarta.faces.context.FacesContext
import jakarta.faces.component.UIComponent
import jakarta.faces.application.FacesMessage

class InRangeValidator(protected val left: Double, protected val right: Double)
    extends Validator[Double]:
  override def validate(
      context: FacesContext,
      component: UIComponent,
      value: Double
  ): Unit =
    if left > value || right < value then
      throw ValidatorException(
        FacesMessage(
          FacesMessage.SEVERITY_ERROR,
          "Out of range",
          "Значение должно быть между %.1f и %.1f".format(left, right)
        )
      )
