package com.itmo.mrdvd.middleware

import zio._
import zio.http.Request
import scala.util.Try

final case class RequestContext(userId: Int)
