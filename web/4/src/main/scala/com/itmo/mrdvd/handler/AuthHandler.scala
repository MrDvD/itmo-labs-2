package com.itmo.mrdvd.handler

import zio.http._
import zio.ZIO
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto._
import scala.util.Success
import com.itmo.mrdvd.service.token.TokenService
import com.itmo.mrdvd.service.crypto.CryptoService
import scala.util.Failure

class AuthHandler(userRepository: CachingRepository[NewUser, StoredUser, String]):
  def login(req: Request): ZIO[CryptoService & TokenService[StoredUser], Nothing, Response] =
    for
      cryptoService <- ZIO.service[CryptoService]
      tokenService <- ZIO.service[TokenService[StoredUser]]
      body <- req.body.asString.orDie
    yield NewUser.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.get(user.login) match
          case Success(storedUser) =>
            if cryptoService.compareHash(cryptoService.hash(user.password), storedUser.passwordHash) then
              Response.json(tokenService.getToken(storedUser))
            else Response.unauthorized
          case Failure(err) =>
            Response.internalServerError(err.toString())
      case Left(err) =>
        Response.badRequest(err.toString()) 

  def register(req: Request): ZIO[TokenService[StoredUser], Nothing, Response] =
    for
      tokenService <- ZIO.service[TokenService[StoredUser]]
      body <- req.body.asString.orDie
    yield NewUser.jsonCodec.decodeJson(body) match
      case Right(user) =>
        userRepository.create(user) match
          case Success(storedUser) =>
            Response.json(tokenService.getToken(storedUser))
          case Failure(err) =>
            Response.internalServerError(err.toString())
      case Left(err) =>
        Response.badRequest(err.toString())
