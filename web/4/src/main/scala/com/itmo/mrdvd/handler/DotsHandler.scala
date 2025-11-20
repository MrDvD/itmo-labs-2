package com.itmo.mrdvd.handler

import zio.http._
import zio._
import zio.json._
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper._
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.repository._
import com.itmo.mrdvd.dto.PrivateRequestContext
import scala.util.Try

class DotsHandler(
    processDotMapper: Mapper[Dot, DotResult],
    dotsRepository: CachingPagedRepository[
      Entry[Int, DotResult],
      Entry[Entry[Int, String], DotResult],
      Int
    ]
):
  def get(req: Request): ZIO[PrivateRequestContext, Nothing, Response] =
    for ctx <- ZIO.service[PrivateRequestContext]
    yield req.queryParam(DotsHandler.pageParam) match
      case Some(page) =>
        Try(page.toInt) match
          case Success(pageNumber) =>
            if pageNumber < 0 then
              Response
                .json(
                  ErrorBatch(query =
                    Some(QueryError(DotsHandler.BadPage))
                  ).toJson
                )
                .status(Status.InternalServerError)
            else
              dotsRepository.getPage(pageNumber, DotsHandler.pageSize) match
                case Success(page) =>
                  Response.json(
                    page
                      .copy(items =
                        page.items
                          .map(entry => Entry(entry.key.value, entry.value))
                      )
                      .toJson
                  )
                case Failure(err) =>
                  Response
                    .json(
                      ErrorBatch(query =
                        Some(QueryError(DotsHandler.UnknownBodyFormat))
                      ).toJson
                    )
                    .status(Status.BadRequest)
          case Failure(_) =>
            Response
              .json(
                ErrorBatch(query = Some(QueryError(DotsHandler.BadPage))).toJson
              )
              .status(Status.InternalServerError)
      case None =>
        Response.json(
          dotsRepository.getAll
            .map(entry => Entry(entry.key.value, entry.value))
            .toArray
            .toJson
        )
  def post(req: Request): ZIO[PrivateRequestContext, Nothing, Response] =
    for
      ctx <- ZIO.service[PrivateRequestContext]
      body <- req.body.asString.orDie
    yield Dot.jsonCodec.decodeJson(body) match
      case Right(dot) =>
        processDotMapper(dot) match
          case Right(result) =>
            dotsRepository.create(Entry(ctx.userId, result)) match
              case Success(created) =>
                Response.json(Entry(created.key.value, created.value).toJson)
              case Failure(_) =>
                Response
                  .json(
                    ErrorBatch(query =
                      Some(
                        QueryError(DotsHandler.ServerError)
                      )
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
      dotsRepository.remove(ctx.userId)
      Response.status(Status.NoContent)

object DotsHandler:
  val UnknownBodyFormat = "Нераспознанный формат запроса"
  val ServerError = "Внутренняя ошибка сервера"
  val BadPage = "Нераспознанный номер страницы данных"

  val pageParam = "page"
  val pageSize = 10
