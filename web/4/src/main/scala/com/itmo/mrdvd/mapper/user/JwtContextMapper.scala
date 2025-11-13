package com.itmo.mrdvd.mapper.user

import com.itmo.mrdvd.mapper.Mapper
import com.itmo.mrdvd.dto.RequestContext
import pdi.jwt.JwtClaim
import pdi.jwt.JwtZIOJson
import scala.util.Success
import scala.util.Failure

class JwtContextMapper extends Mapper[String, RequestContext]:
  override def apply(auth: String): Either[Error, RequestContext] =
    val words = auth.split(" ")
    if words.length >= 2 && words(0) == "Bearer" then
      val jwtToken = words(1)
      JwtZIOJson.decode(jwtToken) match
        case Success(value) =>
          RequestContext.jsonCodec.decodeJson(value.content)
        case Failure(err) =>
          Left(Error("Illegal JWT token")) 
    Left(Error("Unknown authorization protocol"))
