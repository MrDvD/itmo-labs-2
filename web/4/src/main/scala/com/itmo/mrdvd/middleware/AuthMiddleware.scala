package com.itmo.mrdvd.middleware

import zio.http._
import zio.ZIO
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper
import com.itmo.mrdvd.handler.AuthHandler

class AuthMiddleware(contextMapper: Mapper[String, PrivateRequestContext]):
  def parseAuthSession: HandlerAspect[Any, PrivateRequestContext] =
    Middleware.interceptIncomingHandler(
      Handler.fromFunctionZIO[Request]((req: Request) =>
        fillCtx(req)
          .map(ctx => (req, ctx))
          .mapError(_ => Response.unauthorized)
      )
    )

  private def fillCtx(
      req: Request
  ): ZIO[Any, Throwable, PrivateRequestContext] =
    for authorization <- ZIO
        .fromOption(req.cookie(AuthHandler.AuthKey))
        .orElseFail(Error("Found no authorization token"))
    yield contextMapper(authorization.content) match
      case Right(value) => value
      case Left(err)    => throw err
