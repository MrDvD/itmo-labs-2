package com.itmo.mrdvd.service.dotArea

import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.DotResult

trait DotAreaService {
  def addDot(dot: Dot): DotResult
}
