package com.itmo.mrdvd.dto

import zio.schema._
import zio.json.JsonCodec

final case class StoredUser(id: Int, login: String, passwordHash: String)

object StoredUser:
  implicit val schema: Schema[StoredUser] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[StoredUser] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)