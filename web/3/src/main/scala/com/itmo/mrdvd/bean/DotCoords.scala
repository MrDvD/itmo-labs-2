package com.itmo.mrdvd.bean

import com.itmo.mrdvd.dto.Dot
import jakarta.enterprise.context.Dependent
import java.lang.Double

@Dependent
class DotCoords extends Serializable:
  private var x: Double = null
  private var y: Double = null

  def getX(): Double = x
  def getY(): Double = y

  def setX(X: Double): Unit = x = X
  def setY(Y: Double): Unit = y = Y