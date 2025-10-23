package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.dto.Dot
import scala.math.BigDecimal.RoundingMode

class RoundDotMapper extends Mapper[Dot, Dot]:
  override def apply(dot: Dot): Either[Dot, Error] =
    Left(
      Dot(
        BigDecimal.valueOf(dot.X).setScale(2, RoundingMode.HALF_UP).doubleValue,
        BigDecimal.valueOf(dot.Y).setScale(2, RoundingMode.HALF_UP).doubleValue,
        BigDecimal.valueOf(dot.R).setScale(2, RoundingMode.HALF_UP).doubleValue
      )
    )
