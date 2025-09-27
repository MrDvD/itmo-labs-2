package com.itmo.mrdvd.bean

import jakarta.enterprise.context.Dependent
import java.lang.Double
import scala.math.BigDecimal.RoundingMode

@Dependent
class DotCoords extends Serializable:
  private var x: Double = null
  private var y: Double = null

  def getX(): Double = x
  def getY(): Double = y

  def setX(X: Double): Unit = x =
    BigDecimal.valueOf(X).setScale(2, RoundingMode.HALF_UP).doubleValue
  def setY(Y: Double): Unit = y =
    BigDecimal.valueOf(Y).setScale(2, RoundingMode.HALF_UP).doubleValue
