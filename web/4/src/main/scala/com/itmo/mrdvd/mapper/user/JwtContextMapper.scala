package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.mapper.Mapper
import com.itmo.mrdvd.dto.PrivateRequestContext
import pdi.jwt.JwtClaim
import pdi.jwt.JwtZIOJson
import scala.util.Success
import scala.util.Failure

class JwtContextMapper extends Mapper[String, PrivateRequestContext]:
  override def apply(token: String): Either[Error, PrivateRequestContext] =
    JwtZIOJson.decode(token) match
      case Success(value) =>
        PrivateRequestContext.jsonCodec.decodeJson(value.content) match
          case Right(value) => Right(value)
          case Left(err)    => Left(Error(err))
      case Failure(err) =>
        Left(Error("Illegal JWT token"))
