package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.dto.Dot

class RawDotMapper extends Mapper[RawDot, Dot]:
  protected val rangeR = Array[Float](1, 1.5, 2, 2.5, 3)
  override def map(rawDot: RawDot): Option[Dot] =
    val X = rawDot.X.toIntOption
    val Y = rawDot.Y.toFloatOption
    val R = rawDot.R.toFloatOption
    if X.isEmpty || Y.isEmpty || R.isEmpty then
      return Option.empty[Dot]
    val isValidX = Math.abs(X.get) <= 4
    val isValidY = Math.abs(Y.get) <= 5
    val isValidR = this.rangeR.contains(R.get)
    if !isValidX || !isValidY || !isValidR then
      return Option.empty[Dot]
    return Option[Dot](Dot(X.get, Y.get, R.get))
