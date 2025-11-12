package com.itmo.mrdvd.dto

import zio.json._
import zio.schema._

final case class DotResult(dot: Dot, hit: Boolean, date: String)

object DotResult:
  implicit val schema: Schema[DotResult] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[DotResult] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
