package com.itmo.mrdvd.handler

import zio.http._
import zio._
import zio.json._
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper._
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.repository.CachingGroupRepository
import com.itmo.mrdvd.dto.PrivateRequestContext

class DotsHandler(
    processDotMapper: Mapper[Dot, DotResult],
    dotsRepository: CachingGroupRepository[DotResult, DotResult, Int]
):
  def get(req: Request): ZIO[PrivateRequestContext, Nothing, Response] =
    for ctx <- ZIO.service[PrivateRequestContext]
    yield dotsRepository.getGroup(ctx.userId) match
      case Success(value) => Response.json(value.toJson)
      case Failure(_)     =>
        Response
          .json(
            ErrorBatch(query = Some(QueryError(AuthHandler.ServerError))).toJson
          )
          .status(Status.InternalServerError)
  def post(req: Request): ZIO[PrivateRequestContext, Nothing, Response] =
    for
      ctx <- ZIO.service[PrivateRequestContext]
      body <- req.body.asString.orDie
    yield Dot.jsonCodec.decodeJson(body) match
      case Right(dot) =>
        processDotMapper(dot) match
          case Right(result) =>
            dotsRepository.create(ctx.userId, result) match
              case Success(value) =>
                Response.json(result.toJson)
              case Failure(_) =>
                Response
                  .json(
                    ErrorBatch(query =
                      Some(QueryError(AuthHandler.ServerError))
                    ).toJson
                  )
                  .status(Status.InternalServerError)
          case Left(_) =>
            Response
              .json(
                ErrorBatch(query =
                  Some(QueryError(AuthHandler.ServerError))
                ).toJson
              )
              .status(Status.InternalServerError)
      case Left(_) =>
        Response
          .json(
            ErrorBatch(query =
              Some(QueryError(AuthHandler.UnknownBodyFormat))
            ).toJson
          )
          .status(Status.BadRequest)
  def delete(req: Request): ZIO[PrivateRequestContext, Nothing, Response] =
    for ctx <- ZIO.service[PrivateRequestContext]
    yield
      dotsRepository.clearGroup(ctx.userId)
      Response.status(Status.NoContent)

object DotsHandler:
  val UnknownBodyFormat = "Нераспознанный формат запроса"
  val ServerError = "Внутренняя ошибка сервера"
