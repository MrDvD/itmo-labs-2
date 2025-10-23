package com.itmo.mrdvd.dto

case class Dot(X: Double, Y: Double, R: Double):
  def maxCoord(): Double = Math.max(Math.abs(X), Math.abs(Y))
