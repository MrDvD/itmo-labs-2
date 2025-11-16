package com.itmo.mrdvd.dto

import zio.schema._
import zio.json._

final case class NewUser(login: String, password: String)

object NewUser:
  implicit val schema: Schema[NewUser] =
    DeriveSchema
      .gen[NewUser]
      .transformOrFail(
        (user: NewUser) =>
          if user.login.trim != user.login then
            Left("Trim leading and trailing spaces in login")
          if user.password.trim != user.password then
            Left("Trim leading and trailing spaces in password")
          if user.password.length() < 8 then
            Left("Password is shorter than 8 characters")
          Right(user)
        ,
        (user: NewUser) => Right(user)
      )
  implicit val jsonCodec: JsonCodec[NewUser] =
    zio.schema.codec.JsonCodec.jsonCodec(schema)
