package com.itmo.mrdvd.middleware

import zio.http._
import zio.ZIO
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.service.token.TokenService

object AuthMiddleware:
  def parseAuthSession: HandlerAspect[TokenService[StoredUser], RequestContext] =
    Middleware.interceptIncomingHandler(
      Handler.fromFunctionZIO[Request]((req: Request) =>
        fillCtx(req)
          .map(ctx => (req, ctx))
          .mapError(_ => Response.unauthorized)
      )
    )

  private def fillCtx(req: Request): ZIO[TokenService[StoredUser], Throwable, RequestContext] =
    for
      tokenService <- ZIO.service[TokenService[StoredUser]]
      rawUserId <- ZIO
        .fromOption(req.headers.get("Authorization"))
        .orElseFail(Error("Found no authorization token"))
      userId <- ZIO.attempt(rawUserId.toInt)
    yield RequestContext(userId, "? - wip - ?")
