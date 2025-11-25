package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper
import pdi.jwt._
import zio.json.EncoderOps
import java.time.Clock
import com.itmo.mrdvd.AppUtils
import com.itmo.mrdvd.AppParams

class JwtUserMapper extends Mapper[Entry[Int, User], String]:
  implicit val clock: Clock = Clock.systemUTC
  val secret = AppUtils.getEnv(AppParams.secretEnv)
  override def apply(user: Entry[Int, User]): Either[Error, String] =
    val context = PrivateRequestContext(user.key, user.value.login)
    val claim = JwtClaim(context.toJson)
    Right(Jwt.encode(claim.expiresIn(43200), secret(), JwtAlgorithm.HS384))
