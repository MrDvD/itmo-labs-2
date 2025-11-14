package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper
import pdi.jwt._
import zio.json.EncoderOps
import java.time.Clock

class JwtUserMapper extends Mapper[StoredUser, String]:
  implicit val clock: Clock = Clock.systemUTC
  override def apply(user: StoredUser): Either[Error, String] =
    val context = RequestContext(user.id, user.login)
    val claim = JwtClaim(context.toJson)
    Right(Jwt.encode(claim.expiresIn(43200)))
