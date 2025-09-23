package com.itmo.mrdvd.bean

import jakarta.inject.Named
import jakarta.enterprise.context.RequestScoped
import com.itmo.mrdvd.dto.Dot

@Named("dotInput")
@RequestScoped
case class DotInput() extends Serializable:
  private var x: Float = 0
  private var y: Float = 0
  private var r: Float = 0

  def getX(): Float = x
  def getY(): Float = y
  def getR(): Float = r
  def getDot(): Dot = Dot(x, y, r)

  def setX(X: Float): Unit = x = X
  def setY(Y: Float): Unit = y = Y
  def setR(R: Float): Unit = r = R