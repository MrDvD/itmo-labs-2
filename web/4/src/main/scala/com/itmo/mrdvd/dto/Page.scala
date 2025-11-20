package com.itmo.mrdvd.dto

import zio.schema.Schema
import zio.schema.DeriveSchema
import zio.json.JsonCodec

final case class Page[T](
    items: List[T],
    pageNumber: Int,
    pageSize: Int,
    totalItems: Long,
    totalPages: Int
)

object Page:
  implicit def schema[T](implicit
      page: Schema[T]
  ): Schema[Page[T]] = DeriveSchema.gen
  implicit def jsonCodec[T](implicit
      page: Schema[T]
  ): JsonCodec[Page[T]] =
    zio.schema.codec.JsonCodec.jsonCodec(schema[T](page))
