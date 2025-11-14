package com.itmo.mrdvd.dto

import zio.schema._
import zio.json._

final case class ClientState(isAuthorized: Boolean)

object ClientState:
  implicit val schema: Schema[ClientState] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[ClientState] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
