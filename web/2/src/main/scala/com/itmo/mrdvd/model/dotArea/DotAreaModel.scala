package com.itmo.mrdvd.model.dotArea

import com.itmo.mrdvd.dto.Dot

trait DotAreaModel {
  def addDot(dot: Dot): Unit
}
