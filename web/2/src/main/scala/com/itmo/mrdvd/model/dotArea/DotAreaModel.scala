package com.itmo.mrdvd.model.dotArea

import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.AreaResult

trait DotAreaModel {
  def addDot(dot: Dot): AreaResult
}
