package com.itmo.mrdvd.dto

import zio._
import zio.http.Request
import scala.util.Try
import zio.schema._
import zio.json.JsonCodec

final case class PrivateRequestContext(userId: Int, login: String)

object PrivateRequestContext:
  implicit val schema: Schema[PrivateRequestContext] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[PrivateRequestContext] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
