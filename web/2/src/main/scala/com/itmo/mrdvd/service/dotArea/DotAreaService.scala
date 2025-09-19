package com.itmo.mrdvd.service.dotArea

import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.AreaResult

trait DotAreaService {
  def addDot(dot: Dot): AreaResult
}
