package com.itmo.mrdvd.mapper

import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.dto.Dot

class RawDotMapper extends Mapper[RawDot, Dot]:
  protected val rangeR = Array[Float](1, 1.5, 2, 2.5, 3)
  override def apply(rawDot: RawDot): Either[Dot, Error] =
    val X = rawDot.X.toFloatOption
    val Y = rawDot.Y.toFloatOption
    val R = rawDot.R.toFloatOption
    if X.isEmpty || Y.isEmpty || R.isEmpty then
      Right(Error("the sent dot is not fully filled"))
    val isValidX = Math.abs(X.get) <= 4
    val isValidY = Math.abs(Y.get) <= 5
    val isValidR = this.rangeR.contains(R.get)
    if !isValidX || !isValidY || !isValidR then
      Right(Error("the sent dot parameters are not valid"))
    Left(Dot(X.get, Y.get, R.get))
