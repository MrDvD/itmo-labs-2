package com.itmo.mrdvd.middleware

import zio.http._
import zio.ZIO

object AuthMiddleware:
  def parseAuthSession: HandlerAspect[Any, Unit] =
    HandlerAspect.interceptIncomingHandler(
      Handler.fromFunctionZIO[Request](
        request =>
          ZIO.succeed(request, ())
      )
    )