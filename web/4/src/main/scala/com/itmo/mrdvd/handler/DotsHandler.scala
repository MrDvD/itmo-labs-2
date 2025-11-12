package com.itmo.mrdvd.handler

import zio.http._
import zio.URIO
import zio.ZIO
import scala.annotation.switch
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.mapper.RoundDotMapper
import com.itmo.mrdvd.mapper.Mapper
import com.itmo.mrdvd.dto.DotResult

class DotsHandler(processDotMapper: Mapper[Dot, DotResult]):
  def get(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield Response.json("get wip")
  def post(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield Dot.jsonCodec.decodeJson(body) match
      case Right(dot) =>
        processDotMapper(dot) match
          case Right(result) =>
            Response.json(DotResult.jsonCodec.encodeJson(result, Some(0)))
          case Left(err) =>
            Response.internalServerError
      case Left(err) =>
        Response.badRequest
  def delete(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield Response.json("delete wip")
