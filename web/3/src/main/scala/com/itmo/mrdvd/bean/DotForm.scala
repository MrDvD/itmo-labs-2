package com.itmo.mrdvd.bean

import jakarta.inject.Named;
import jakarta.enterprise.context.ApplicationScoped

@Named("dotForm")
@ApplicationScoped
class DotForm extends Serializable:
  private val yValues = Array(-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2)
  private val rValues = Array(1, 1.5, 2, 2.5, 3)
  
  def getRangeY(): Array[Double] = yValues
  def getRangeR(): Array[Double] = rValues