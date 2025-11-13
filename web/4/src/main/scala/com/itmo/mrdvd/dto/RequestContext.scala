package com.itmo.mrdvd.dto

import zio._
import zio.http.Request
import scala.util.Try
import zio.schema._
import zio.json.JsonCodec

final case class RequestContext(userId: Int, login: String)

object RequestContext:
  implicit val schema: Schema[RequestContext] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[RequestContext] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
