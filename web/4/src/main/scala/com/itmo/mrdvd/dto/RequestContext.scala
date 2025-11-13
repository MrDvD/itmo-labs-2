package com.itmo.mrdvd.dto

import zio._
import zio.http.Request
import scala.util.Try

final case class RequestContext(userId: Int, login: String)
