package com.itmo.mrdvd.service.crypto

import zio.ZLayer

class Argon2CryptoService extends CryptoService:
  override def compareHash(str1: String, str2: String): Boolean = ???
  override def hash(str1: String): String = ???

object Argon2CryptoService:
  val live = ZLayer.succeed(Argon2CryptoService())