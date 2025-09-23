package com.itmo.mrdvd.service.dotArea

import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.DotResult
import java.time.format.DateTimeFormatter
import java.time.ZonedDateTime
import java.time.ZoneId
import jakarta.enterprise.context.ApplicationScoped

@ApplicationScoped
class Lab3DotAreaService extends DotAreaService:
  val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
  val zone = ZoneId.of("Europe/Moscow")
  override def addDot(dot: Dot): DotResult =
    val inCircle = dot.X >= 0 && dot.Y >= 0 && Math.pow(dot.X, 2) + Math.pow(dot.Y, 2) <= Math.pow(dot.R, 2)
    val inSquare = Math.min(dot.X, dot.Y) >= 0 && Math.max(dot.X, dot.Y) <= dot.R
    val inTriangle = dot.X <= 0 && dot.X >= -dot.R && dot.Y >= 0 && 2 * dot.Y <= dot.X + dot.R
    return DotResult(dot, inCircle || inSquare || inTriangle, ZonedDateTime.now(zone).format(formatter))
