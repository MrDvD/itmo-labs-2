package com.itmo.mrdvd

import zio._
import zio.http._
import zio.http.template._
import java.io.File
import com.itmo.mrdvd.handler.DotsHandler

object App extends ZIOAppDefault:
  val dotsHandler = DotsHandler()
  val dotsRoutes = Routes(
    Method.GET / "dots" -> handler(dotsHandler.get),
    Method.POST / "dots" -> handler(dotsHandler.post),
    Method.DELETE / "dots" -> handler(dotsHandler.delete)
  )
  val staticRoutes = Routes(
    Method.GET / trailing -> Handler.fromFile(File(AppPath.index)).orDie
  )
  val app =
    staticRoutes ++ dotsRoutes ++ Routes.empty @@
      Middleware.serveDirectory(
        Path.empty / "assets",
        File(AppPath.assets)
      )
  def run = Server.serve(app).provide(Server.default)

object AppPath:
  val index = "dist/index.html"
  val assets = "dist/assets"
