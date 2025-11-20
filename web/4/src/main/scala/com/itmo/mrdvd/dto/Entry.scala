package com.itmo.mrdvd.dto

import zio.schema.Schema
import zio.schema.DeriveSchema
import zio.json.JsonCodec

final case class Entry[Key, Val](key: Key, value: Val)

object Entry:
  implicit def schema[Key, Val](implicit
      key: Schema[Key],
      value: Schema[Val]
  ): Schema[Entry[Key, Val]] = DeriveSchema.gen
  implicit def jsonCodec[Key, Val](implicit
      key: Schema[Key],
      value: Schema[Val]
  ): JsonCodec[Entry[Key, Val]] =
    zio.schema.codec.JsonCodec.jsonCodec(schema[Key, Val](key, value))
