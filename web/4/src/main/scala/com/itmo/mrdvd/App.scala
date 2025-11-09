package com.itmo.mrdvd

import zio._
import zio.http._
import zio.http.template._
import java.io.File

object App extends ZIOAppDefault:
  val apiRoutes = Routes(
    Method.GET / "hello" -> Handler.text("hi there")
  )
  val staticRoutes = Routes(
    Method.GET / trailing -> Handler.fromFile(File("dist/index.html")).orDie
  )
  val app =
    staticRoutes ++ apiRoutes ++ Routes.empty @@ Middleware.serveDirectory(
      Path.empty / "assets",
      File("dist/assets")
    )
  def run = Server.serve(app).provide(Server.default)
