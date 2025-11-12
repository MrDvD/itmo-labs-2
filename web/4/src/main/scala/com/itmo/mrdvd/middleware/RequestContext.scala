package com.itmo.mrdvd.middleware

import zio.ZLayer
import zio.ZIO
import zio.http.Request
import scala.util.Try

final case class RequestContext(userId: Int)
