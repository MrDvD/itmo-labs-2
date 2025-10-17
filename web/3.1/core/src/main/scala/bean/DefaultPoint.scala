package com.itmo.mrdvd.bean

import jakarta.faces.view.ViewScoped
import java.lang.Double
import jakarta.inject.Named
import scala.math.BigDecimal.RoundingMode

@Named
@ViewScoped
class DefaultPoint extends Serializable:
  private var X: Double = 0
  private var Y: Double = 0
  private var R: Double = 0

  def getX(): Double = X
  def getY(): Double = Y
  def getR(): Double = R

  def setX(x: Double): Unit = X = x
  def setY(y: Double): Unit = Y = y
  def setR(r: Double): Unit = R = r
