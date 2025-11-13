package com.itmo.mrdvd.service.token

import com.itmo.mrdvd.dto.StoredUser
import zio.ZLayer

class JwtTokenService extends TokenService[StoredUser]:
  def getToken(obj: StoredUser): String = ???

object JwtTokenService:
  val live = ZLayer.succeed(JwtTokenService())