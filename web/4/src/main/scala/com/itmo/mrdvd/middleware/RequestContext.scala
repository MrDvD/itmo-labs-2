package com.itmo.mrdvd.middleware

import zio.ZLayer
import zio.ZIO
import zio.http.Request
import scala.util.Try

final case class RequestContext(userId: Int)

object RequestContext:
  val layer: ZLayer[Request, Throwable, RequestContext] =
    ZLayer.scoped(
      for
        req <- ZIO.service[Request]
        ctx <- fillCtx(req)
      yield ctx
    )
  
  private def fillCtx(req: Request): ZIO[Any, Throwable, RequestContext] =
    for
      rawUserId <- ZIO.fromOption(req.headers.get("Authentication")).orElseFail(Error("Found no authentication token"))
      userId <- ZIO.attempt(rawUserId.toInt)
    yield RequestContext(userId)
