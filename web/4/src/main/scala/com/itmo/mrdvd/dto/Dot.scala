package com.itmo.mrdvd.dto

import zio.json._
import zio.schema._

final case class Dot(X: Double, Y: Double, R: Double):
  def maxCoord(): Double = Math.max(Math.abs(X), Math.abs(Y))

object Dot:
  implicit val schema: Schema[Dot] =
    DeriveSchema
      .gen[Dot]
      .transformOrFail(
        (dot: Dot) =>
          val doesFit = (x: Double) => math.abs(x) <= 3
          if doesFit(dot.X) && doesFit(dot.Y) && doesFit(dot.R) && dot.R >= 0
          then Right(dot)
          else Left("Dot does not fit")
        ,
        (dot: Dot) => Right(dot)
      )
  implicit val jsonCodec: JsonCodec[Dot] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
