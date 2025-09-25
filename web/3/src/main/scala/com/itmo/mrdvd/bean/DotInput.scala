package com.itmo.mrdvd.bean

import com.itmo.mrdvd.dto.Dot
import jakarta.enterprise.context.Dependent
import java.lang.Double

@Dependent
class DotInput() extends Serializable:
  private var x: Double = null
  private var y: Double = null
  private var r: Double = null

  def getX(): Double = x
  def getY(): Double = y
  def getR(): Double = r
  def getDot(): Dot = Dot(x, y, r)

  def setX(X: Double): Unit = x = X
  def setY(Y: Double): Unit = y = Y
  def setR(R: Double): Unit = r = R