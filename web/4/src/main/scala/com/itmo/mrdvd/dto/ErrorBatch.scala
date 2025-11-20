package com.itmo.mrdvd.dto

import zio.schema._
import zio.json.JsonCodec

final case class ValidationError(name: String, message: String)
final case class QueryError(message: String)
final case class ErrorBatch(
    validation: Option[List[ValidationError]] = None,
    query: Option[QueryError] = None
)

object ErrorBatch:
  implicit val schema: Schema[ErrorBatch] = DeriveSchema.gen
  implicit val jsonCodec: JsonCodec[ErrorBatch] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
