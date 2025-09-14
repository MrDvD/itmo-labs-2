package com.itmo.mrdvd.model.dotArea

import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.AreaResult
import java.time.LocalDateTime

class Lab2DotAreaModel extends DotAreaModel {
  override def addDot(dot: Dot): AreaResult =
    val inCircle = dot.X >= 0 && dot.Y <= 0 && Math.pow(dot.X, 2) + Math.pow(dot.Y, 2) <= Math.pow(dot.R, 2)
    val inTrapezoid = dot.X >= -dot.R && dot.X <= 0 && dot.Y <= dot.R / 2 && dot.Y >= -dot.X - dot.R
    return AreaResult(dot, inCircle || inTrapezoid, LocalDateTime.now().toString())
}
