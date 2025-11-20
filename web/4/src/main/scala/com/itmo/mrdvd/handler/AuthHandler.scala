package com.itmo.mrdvd.handler

import zio.http._
import zio.ZIO
import zio.json.EncoderOps
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto._
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.mapper.Mapper
import com.outr.scalapass.PasswordFactory
import zio.http.Cookie.SameSite
import zio.Duration
import java.util.concurrent.TimeUnit
import java.util.Base64

class AuthHandler(
    userRepository: CachingRepository[User, Entry[Int, User], String],
    tokenProducer: Mapper[Entry[Int, User], String]
):
  def login(
      req: Request
  ): ZIO[PasswordFactory, Nothing, Response] =
    for
      cryptoService <- ZIO.service[PasswordFactory]
      body <- req.body.asString.orDie
    yield User.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.get(user.login) match
          case Success(storedUser) =>
            if cryptoService.verify(user.password, storedUser.value.password)
            then
              tokenProducer(storedUser) match
                case Right(token) =>
                  Response
                    .json(ClientState(true, user.login).toJson)
                    .addCookie(
                      Cookie
                        .Response(
                          AuthHandler.AuthKey,
                          token,
                          isHttpOnly = true,
                          path = Some(Path.root)
                        )
                    )
                    .addCookie(
                      Cookie.Response(
                        AuthHandler.ClientState,
                        Base64.getEncoder.encodeToString(
                          ClientState(true, user.login).toJson.getBytes
                        ),
                        path = Some(Path.root)
                      )
                    )
                case Left(_) =>
                  Response
                    .json(
                      ErrorBatch(query =
                        Some(QueryError(AuthHandler.ServerError))
                      ).toJson
                    )
                    .status(Status.InternalServerError)
            else
              Response
                .json(
                  ErrorBatch(query =
                    Some(QueryError(AuthHandler.InvalidLoginAttempt))
                  ).toJson
                )
                .status(Status.Unauthorized)
          case Failure(_) =>
            Response
              .json(
                ErrorBatch(query =
                  Some(QueryError(AuthHandler.InvalidLoginAttempt))
                ).toJson
              )
              .status(Status.Unauthorized)
      case Left(_) =>
        Response
          .json(
            ErrorBatch(query =
              Some(QueryError(AuthHandler.UnknownBodyFormat))
            ).toJson
          )
          .status(Status.BadRequest)

  def register(req: Request): ZIO[PasswordFactory, Nothing, Response] =
    for
      cryptoService <- ZIO.service[PasswordFactory]
      body <- req.body.asString.orDie
    yield User.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.create(
          user.copy(password = cryptoService.hash(user.password))
        ) match
          case Success(storedUser) =>
            tokenProducer(storedUser) match
              case Right(token) =>
                Response
                  .json(ClientState(true, user.login).toJson)
                  .addCookie(
                    Cookie
                      .Response(
                        AuthHandler.AuthKey,
                        token,
                        isHttpOnly = true,
                        path = Some(Path.root),
                        maxAge = Some(Duration(24, TimeUnit.HOURS))
                      )
                  )
                  .addCookie(
                    Cookie.Response(
                      AuthHandler.ClientState,
                      Base64.getEncoder.encodeToString(
                        ClientState(true, user.login).toJson.getBytes
                      ),
                      path = Some(Path.root),
                      maxAge = Some(Duration(24, TimeUnit.HOURS))
                    )
                  )
              case Left(_) =>
                Response
                  .json(
                    ErrorBatch(query =
                      Some(QueryError(AuthHandler.ServerError))
                    ).toJson
                  )
                  .status(Status.InternalServerError)
          case Failure(_) =>
            Response
              .json(
                ErrorBatch(query =
                  Some(QueryError(AuthHandler.UserCreationFailure))
                ).toJson
              )
              .status(Status.BadRequest)
      case Left(_) =>
        Response
          .json(
            ErrorBatch(query =
              Some(QueryError(AuthHandler.UnknownBodyFormat))
            ).toJson
          )
          .status(Status.BadRequest)

  def exit(req: Request): ZIO[Any, Nothing, Response] =
    ZIO.succeed(
      Response
        .status(Status.NoContent)
        .addCookie(
          Cookie.Response(
            AuthHandler.AuthKey,
            "",
            isHttpOnly = true,
            path = Some(Path.root),
            maxAge = Some(Duration(0, TimeUnit.SECONDS))
          )
        )
        .addCookie(
          Cookie.Response(
            AuthHandler.ClientState,
            Base64.getEncoder
              .encodeToString(ClientState(false, "").toJson.getBytes),
            path = Some(Path.root),
            maxAge = Some(Duration(0, TimeUnit.SECONDS))
          )
        )
    )

object AuthHandler:
  val AuthKey = "token"
  val ClientState = "client-state"

  val InvalidLoginAttempt = "Неудачная попытка аутентификации"
  val UnknownBodyFormat = "Нераспознанный формат запроса"
  val UserCreationFailure = "Не удалось зарегистрировать пользователя"
  val ServerError = "Внутренняя ошибка сервера"
