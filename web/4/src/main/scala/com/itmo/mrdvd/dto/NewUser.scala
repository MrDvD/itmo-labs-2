package com.itmo.mrdvd.dto

import zio.schema._
import zio.json.JsonCodec

final case class NewUser(login: String, password: String)

object NewUser:
  implicit val schema: Schema[NewUser] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[NewUser] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)