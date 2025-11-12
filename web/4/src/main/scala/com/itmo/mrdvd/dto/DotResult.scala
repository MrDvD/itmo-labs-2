package com.itmo.mrdvd.dto

import zio.json._
import zio.schema._

case class DotResult(dot: Dot, hit: Boolean, date: String)

object DotResult:
  implicit val schema: Schema[Dot] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[DotResult] = DeriveJsonCodec.gen
