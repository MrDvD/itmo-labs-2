package com.itmo.mrdvd.middleware

import zio.http._
import zio.ZIO
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper

class AuthMiddleware(contextMapper: Mapper[String, RequestContext]):
  def parseAuthSession: HandlerAspect[Any, RequestContext] =
    Middleware.interceptIncomingHandler(
      Handler.fromFunctionZIO[Request]((req: Request) =>
        fillCtx(req)
          .map(ctx => (req, ctx))
          .mapError(_ => Response.unauthorized)
      )
    )

  private def fillCtx(
      req: Request
  ): ZIO[Any, Throwable, RequestContext] =
    for authorization <- ZIO
        .fromOption(req.headers.get("Authorization"))
        .orElseFail(Error("Found no authorization token"))
    yield contextMapper(authorization) match
      case Right(value) => value
      case Left(err)    => throw err
