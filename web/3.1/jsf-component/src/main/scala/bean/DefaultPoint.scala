package com.itmo.mrdvd.bean

import jakarta.faces.view.ViewScoped
import java.lang.Double
import jakarta.inject.Named

@Named
@ViewScoped
class DefaultPoint extends Serializable:
  private var X: Double = null
  private var Y: Double = null
  private var R: Double = null

  def getX(): Double = X
  def getY(): Double = Y
  def getR(): Double = R

  def setX(x: Double): Unit = X = x
  def setY(y: Double): Unit = Y = y
  def setR(r: Double): Unit = R = r
