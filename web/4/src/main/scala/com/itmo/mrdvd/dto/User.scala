package com.itmo.mrdvd.dto

import zio.schema._
import zio.json._

final case class User(login: String, password: String)

object User:
  implicit val schema: Schema[User] =
    DeriveSchema
      .gen[User]
      .transformOrFail(
        (user: User) =>
          if user.login.trim != user.login then
            Left("Trim leading and trailing spaces in login")
          if user.password.trim != user.password then
            Left("Trim leading and trailing spaces in password")
          if user.password.length() < 8 then
            Left("Password is shorter than 8 characters")
          Right(user)
        ,
        (user: User) => Right(user)
      )
  implicit val jsonCodec: JsonCodec[User] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
