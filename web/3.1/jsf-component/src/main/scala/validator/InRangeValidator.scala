package com.itmo.mrdvd.validator

import jakarta.faces.validator.{Validator, ValidatorException}
import jakarta.faces.context.FacesContext
import jakarta.faces.component.UIComponent
import jakarta.faces.application.FacesMessage
import jakarta.faces.validator.FacesValidator
import jakarta.faces.component.FacesComponent

@FacesValidator
class InRangeValidator extends Validator[Double]:
  override def validate(
      context: FacesContext,
      component: UIComponent,
      value: Double
  ): Unit =
    val min = component.getAttributes().get("min").asInstanceOf[Double]
    val max = component.getAttributes().get("max").asInstanceOf[Double]
    if min > value || max < value then
      throw ValidatorException(
        FacesMessage(
          FacesMessage.SEVERITY_ERROR,
          "Out of range",
          "Значение должно быть между %.1f и %.1f".format(min, max)
        )
      )
