package com.itmo.mrdvd.middleware

import zio.http._
import zio.ZIO

object AuthMiddleware:
  def parseAuthSession: HandlerAspect[Any, RequestContext] =
    Middleware.interceptIncomingHandler(
      Handler.fromFunctionZIO[Request](
        (req: Request) => 
        fillCtx(req)
        .map(ctx => (req, ctx))
        .mapError(_ => Response.unauthorized)
      )
    )
  
  private def fillCtx(req: Request): ZIO[Any, Throwable, RequestContext] =
    for
      rawUserId <- ZIO.fromOption(req.headers.get("Authentication")).orElseFail(Error("Found no authentication token"))
      userId <- ZIO.attempt(rawUserId.toInt)
    yield RequestContext(userId)