package com.itmo.mrdvd.dto

import zio.json._

case class Dot(X: Double, Y: Double, R: Double):
  def maxCoord(): Double = Math.max(Math.abs(X), Math.abs(Y))

object Dot:
  implicit val jsonCodec: JsonCodec[Dot] = DeriveJsonCodec.gen
