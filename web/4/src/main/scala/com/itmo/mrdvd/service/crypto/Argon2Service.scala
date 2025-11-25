package com.itmo.mrdvd.service.crypto

import com.outr.scalapass.Argon2PasswordFactory
import zio.ZLayer
import com.outr.scalapass.Argon2

class Argon2Service(
    iterations: Int = Argon2PasswordFactory.iterations,
    memory: Int = Argon2PasswordFactory.memory,
    parallelism: Int = Argon2PasswordFactory.parallelism,
    argon2: Argon2 = Argon2.id,
    saltLength: Int = Argon2.saltLength,
    hashLength: Int = Argon2.hashLength
) extends Argon2PasswordFactory(
      iterations,
      memory,
      parallelism,
      argon2,
      saltLength,
      hashLength
    )

object Argon2Service:
  val live = ZLayer.succeed(
    Argon2Service(
      parallelism = 4,
      saltLength = 16,
      hashLength = 16,
      memory = 1024,
      iterations = 2
    )
  )
