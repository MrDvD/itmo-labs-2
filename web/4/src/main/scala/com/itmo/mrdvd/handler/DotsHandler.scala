package com.itmo.mrdvd.handler

import zio.http._
import zio.URIO
import zio.ZIO

class DotsHandler:
  def get(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield Response.json("get wip")
  def post(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield Response.json("post wip")
  def delete(req: Request): ZIO[Any, Nothing, Response] =
    for body <- req.body.asString.orDie
    yield Response.json("delete wip")
