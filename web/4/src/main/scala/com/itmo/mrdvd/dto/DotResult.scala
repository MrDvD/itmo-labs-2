package com.itmo.mrdvd.dto

import zio.json._

case class DotResult(dot: Dot, hit: Boolean, date: String)

object DotResult:
  implicit val jsonCodec: JsonCodec[DotResult] = DeriveJsonCodec.gen
