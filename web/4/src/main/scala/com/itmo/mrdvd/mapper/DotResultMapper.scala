package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.dto.{Dot, DotResult}
import java.time.format.DateTimeFormatter
import java.time.{ZoneId, ZonedDateTime}

class DotResultMapper(roundDotMapper: Mapper[Dot, Dot])
    extends Mapper[Dot, DotResult]:
  val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
  val zone = ZoneId.of("Europe/Moscow")
  override def apply(dot: Dot): Either[Error, DotResult] =
    val inCircle = dot.X <= 0 && dot.Y <= 0 && Math.pow(dot.X, 2) + Math.pow(
      dot.Y,
      2
    ) <= Math.pow(dot.R / 2, 2)
    val inRectangle =
      -dot.R / 2 <= dot.X && dot.X <= 0 && 0 <= dot.Y && dot.Y <= dot.R
    val inTriangle =
      0 <= dot.X && dot.X <= dot.R && 0 <= dot.Y && dot.Y <= dot.R / 2 && dot.Y <= -dot.X / 2 + dot.R / 2
    roundDotMapper(dot) match
      case Right(value) =>
        Right(
          DotResult(
            value,
            inCircle || inRectangle || inTriangle,
            ZonedDateTime.now(zone).format(formatter)
          )
        )
      case Left(value) => Left(value)
