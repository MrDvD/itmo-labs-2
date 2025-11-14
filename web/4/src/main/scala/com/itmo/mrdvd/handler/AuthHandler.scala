package com.itmo.mrdvd.handler

import zio.http._
import zio.ZIO
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto._
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.mapper.Mapper
import com.outr.scalapass.PasswordFactory
import zio.http.Cookie.SameSite

class AuthHandler(
    userRepository: CachingRepository[NewUser, StoredUser, String],
    tokenProducer: Mapper[StoredUser, String]
):
  def login(
      req: Request
  ): ZIO[PasswordFactory, Nothing, Response] =
    for
      cryptoService <- ZIO.service[PasswordFactory]
      body <- req.body.asString.orDie
    yield NewUser.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.get(user.login) match
          case Success(storedUser) =>
            if cryptoService.verify(user.password, storedUser.passwordHash) then
              tokenProducer(storedUser) match
                case Right(token) =>
                  Response
                    .status(Status.NoContent)
                    .addCookie(
                      Cookie
                        .Response(
                          AuthHandler.AuthKey,
                          token,
                          isHttpOnly = true,
                          path = Some(Path.root)
                        )
                    )
                case Left(err) =>
                  Response.internalServerError(err.getMessage())
            else Response.unauthorized
          case Failure(err) =>
            Response.unauthorized(err.getMessage())
      case Left(err) =>
        Response.badRequest(err)

  def register(req: Request): ZIO[PasswordFactory, Nothing, Response] =
    for
      cryptoService <- ZIO.service[PasswordFactory]
      body <- req.body.asString.orDie
    yield NewUser.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.create(
          user.copy(password = cryptoService.hash(user.password))
        ) match
          case Success(storedUser) =>
            tokenProducer(storedUser) match
              case Right(token) =>
                Response
                  .status(Status.NoContent)
                  .addCookie(
                    Cookie
                      .Response(
                        AuthHandler.AuthKey,
                        token,
                        isHttpOnly = true,
                        path = Some(Path.root)
                      )
                  )
              case Left(err) =>
                Response.internalServerError(err.getMessage())
          case Failure(err) =>
            Response.internalServerError(err.getMessage())
      case Left(err) =>
        Response.badRequest(err)

  def exit(req: Request): ZIO[Any, Nothing, Response] =
    ZIO.succeed(
      Response
        .status(Status.NoContent)
        .addCookie(Cookie.clear(AuthHandler.AuthKey))
    )

object AuthHandler:
  val AuthKey = "token"
