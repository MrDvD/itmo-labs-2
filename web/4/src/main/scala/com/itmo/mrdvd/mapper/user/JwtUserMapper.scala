package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.dto.StoredUser
import com.itmo.mrdvd.mapper.Mapper
import com.itmo.mrdvd.dto.RequestContext
import pdi.jwt.JwtClaim
import zio.json.EncoderOps
import java.time.Clock

class JwtUserMapper extends Mapper[StoredUser, String]:
  implicit val clock: Clock = Clock.systemUTC
  override def apply(user: StoredUser): Either[Error, String] =
    val context = RequestContext(user.id, user.login)
    val claim = JwtClaim(context.toJson)
    Right(claim.expiresIn(43200).toJson)
