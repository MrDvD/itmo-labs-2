package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.mapper.Mapper
import com.outr.scalapass.Argon2PasswordFactory

class Argon2StringMapper extends Mapper[String, String]:
  val factory = Argon2PasswordFactory(
    parallelism = 4,
    saltLength = 16,
    hashLength = 16,
    memory = 1024,
    iterations = 2
  )
  override def apply(str: String): Either[Error, String] =
    Right(factory.hash(str))