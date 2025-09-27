package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.dto.{Dot, DotResult}
import java.time.format.DateTimeFormatter
import java.time.{ZoneId, ZonedDateTime}
import jakarta.enterprise.context.ApplicationScoped

@ApplicationScoped
class DotResultMapper extends Mapper[Dot, DotResult]:
  val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
  val zone = ZoneId.of("Europe/Moscow")
  override def apply(dot: Dot): Either[DotResult, Error] =
    val inCircle = dot.X >= 0 && dot.Y >= 0 && Math.pow(dot.X, 2) + Math.pow(
      dot.Y,
      2
    ) <= Math.pow(dot.R / 2, 2)
    val inSquare =
      Math.min(dot.X, -dot.Y) >= 0 && Math.max(dot.X, -dot.Y) <= dot.R
    val inTriangle =
      dot.X <= 0 && dot.X >= -dot.R && dot.Y >= 0 && 2 * dot.Y <= dot.X + dot.R
    Left(
      DotResult(
        dot,
        inCircle || inSquare || inTriangle,
        ZonedDateTime.now(zone).format(formatter)
      )
    )
