package com.itmo.mrdvd.handler

import zio.http._
import zio._
import zio.json._
import scala.annotation.switch
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.mapper._
import com.itmo.mrdvd.dto.DotResult
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.repository.CachingGroupRepository
import com.itmo.mrdvd.middleware.RequestContext

class DotsHandler(
    processDotMapper: Mapper[Dot, DotResult],
    dotsRepository: CachingGroupRepository[DotResult, DotResult, Int]
):
  def get(req: Request): ZIO[Any, Nothing, Response] =
    ZIO.succeed(
      Response.json(dotsRepository.getAll.toJson)
    )
  def post(req: Request): ZIO[RequestContext, Nothing, Response] =
    for
      ctx <- ZIO.service[RequestContext]
      body <- req.body.asString.orDie
    yield Dot.jsonCodec.decodeJson(body) match
      case Right(dot) =>
        processDotMapper(dot) match
          case Right(result) =>
            dotsRepository.create(ctx.userId, result) match
              case Success(value) =>
                Response.json(result.toJson)
              case Failure(err) =>
                Response.internalServerError(err.toString())
          case Left(err) =>
            Response.internalServerError(err.toString())
      case Left(err) =>
        Response.badRequest
  def delete(req: Request): ZIO[Any, Nothing, Response] =
    dotsRepository.clearAll
    ZIO.succeed(
      Response.status(Status.NoContent)
    )
