package com.itmo.mrdvd

import zio._
import zio.http._

object App extends ZIOAppDefault:
  val routes = Routes(
    Method.GET / "hello" -> Handler.text("hi there")
  )
  def run = Server.serve(routes).provide(Server.default)
