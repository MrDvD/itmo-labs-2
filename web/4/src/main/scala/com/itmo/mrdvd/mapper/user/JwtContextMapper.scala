package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.mapper.Mapper
import com.itmo.mrdvd.dto.PrivateRequestContext
import pdi.jwt.JwtClaim
import pdi.jwt.JwtZIOJson
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.AppUtils
import com.itmo.mrdvd.AppParams
import pdi.jwt.JwtAlgorithm

class JwtContextMapper extends Mapper[String, PrivateRequestContext]:
  val secret = AppUtils.getEnv(AppParams.secretEnv)
  override def apply(token: String): Either[Error, PrivateRequestContext] =
    JwtZIOJson.decode(token, secret(), Seq(JwtAlgorithm.HS384)) match
      case Success(value) =>
        PrivateRequestContext.jsonCodec
          .decodeJson(value.content)
          .left
          .map(err => Error(err))
      case Failure(err) =>
        Left(Error("Illegal JWT token"))
