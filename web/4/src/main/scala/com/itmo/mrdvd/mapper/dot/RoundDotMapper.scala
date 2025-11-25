package com.itmo.mrdvd.mapper.dot

import com.itmo.mrdvd.dto.Dot
import scala.math.BigDecimal.RoundingMode
import com.itmo.mrdvd.mapper.Mapper

class RoundDotMapper extends Mapper[Dot, Dot]:
  override def apply(dot: Dot): Either[Error, Dot] =
    Right(
      Dot(
        BigDecimal.valueOf(dot.X).setScale(2, RoundingMode.HALF_UP).doubleValue,
        BigDecimal.valueOf(dot.Y).setScale(2, RoundingMode.HALF_UP).doubleValue,
        BigDecimal.valueOf(dot.R).setScale(2, RoundingMode.HALF_UP).doubleValue
      )
    )
