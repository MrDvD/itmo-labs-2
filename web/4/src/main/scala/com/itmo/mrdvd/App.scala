package com.itmo.mrdvd

import zio._
import zio.http._
import zio.http.template._
import java.io.File
import com.itmo.mrdvd.handler.DotsHandler
import com.itmo.mrdvd.middleware._
import com.itmo.mrdvd.mapper._
import com.itmo.mrdvd.mapper.dot._
import com.itmo.mrdvd.repository.dot._
import com.itmo.mrdvd.handler.AuthHandler
import com.itmo.mrdvd.repository.user.UserCachingRepository
import com.itmo.mrdvd.repository.user.UserJdbcRepository
import com.itmo.mrdvd.mapper.user.UserResultMapper
import com.itmo.mrdvd.mapper.user.JwtUserMapper
import com.itmo.mrdvd.mapper.user.JwtContextMapper
import com.itmo.mrdvd.mapper.user.Argon2StringMapper

object App extends ZIOAppDefault:
  val dotsHandler = DotsHandler(
    DotResultMapper(RoundDotMapper()),
    DotResultCachingRepository(DotResultJdbcRepository(UserDotMapper()))
  )
  val authHandler = AuthHandler(
    UserCachingRepository(UserJdbcRepository(UserResultMapper())),
    JwtUserMapper(),
    Argon2StringMapper()
  )
  val authMiddleware = AuthMiddleware(JwtContextMapper())
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
  val authRoutes = Routes(
    Method.POST / "api" / AppParams.apiVersion / "login" -> handler(
      authHandler.login
    ),
    Method.POST / "api" / AppParams.apiVersion / "register" -> handler(
      authHandler.register
    )
  )
  val staticRoutes = Routes(
    Method.GET / trailing -> Handler.fromFile(File(AppParams.index)).orDie
  )
  val app =
    staticRoutes ++ dotsRoutes @@ authMiddleware.parseAuthSession ++ authRoutes ++ Routes.empty @@
      Middleware.serveDirectory(
        Path.empty / "assets",
        File(AppParams.assets)
      )
  def run = Server
    .serve(app)
    .provide(Server.default)

object AppParams:
  val index = "dist/index.html"
  val assets = "dist/assets"
  val apiVersion = "1"
