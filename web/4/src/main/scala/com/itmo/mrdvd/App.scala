package com.itmo.mrdvd

import zio._
import zio.http._
import zio.http.template._
import java.io.File
import com.itmo.mrdvd.handler.DotsHandler
import com.itmo.mrdvd.middleware._
import com.itmo.mrdvd.mapper._
import com.itmo.mrdvd.repository.dot._

object App extends ZIOAppDefault:
  val dotsHandler = DotsHandler(
    DotResultMapper(RoundDotMapper()),
    DotResultCachingRepository(DotResultJdbcRepository(UserDotMapper()))
  )
  val dotsRoutes = Routes(
    Method.GET / "api" / AppParams.apiVersion / "dots" -> handler(
      dotsHandler.get
    ),
    Method.POST / "api" / AppParams.apiVersion / "dots" -> handler(
      dotsHandler.post
    ),
    Method.DELETE / "api" / AppParams.apiVersion / "dots" -> handler(
      dotsHandler.delete
    )
  )
  val staticRoutes = Routes(
    Method.GET / trailing -> Handler.fromFile(File(AppParams.index)).orDie
  )
  val app =
    staticRoutes ++ dotsRoutes @@ AuthMiddleware.parseAuthSession ++ Routes.empty @@
      Middleware.serveDirectory(
        Path.empty / "assets",
        File(AppParams.assets)
      )
  def run = Server.serve(app).provide(Server.default)

object AppParams:
  val index = "dist/index.html"
  val assets = "dist/assets"
  val apiVersion = "1"
