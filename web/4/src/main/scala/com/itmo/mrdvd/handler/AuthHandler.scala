package com.itmo.mrdvd.handler

import zio.http._
import zio.ZIO
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto._
import scala.util.Success
import scala.util.Failure
import com.itmo.mrdvd.mapper.Mapper

class AuthHandler(
    userRepository: CachingRepository[NewUser, StoredUser, String],
    tokenProducer: Mapper[StoredUser, String],
    cryptoMap: Mapper[String, String]
):
  def login(
      req: Request
  ): ZIO[Any, Nothing, Response] =
    for
      body <- req.body.asString.orDie
    yield NewUser.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.get(user.login) match
          case Success(storedUser) =>
            cryptoMap(user.password) match
              case Right(hash) =>
                if hash == storedUser.passwordHash then
                  tokenProducer(storedUser) match
                    case Right(value) => Response.json(value)
                    case Left(err) => Response.internalServerError(err.toString())
                else Response.unauthorized
              case Left(err) =>
                Response.internalServerError(err.toString())
          case Failure(err) =>
            Response.internalServerError(err.toString())
      case Left(err) =>
        Response.badRequest(err.toString())

  def register(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield NewUser.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.create(user) match
          case Success(storedUser) =>
            tokenProducer(storedUser) match
              case Right(value) => Response.json(value)
              case Left(err)    => Response.internalServerError(err.toString())
          case Failure(err) =>
            Response.internalServerError(err.toString())
      case Left(err) =>
        Response.badRequest(err.toString())
