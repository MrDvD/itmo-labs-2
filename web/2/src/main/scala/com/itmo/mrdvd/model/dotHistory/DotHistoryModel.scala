package com.itmo.mrdvd.model.dotHistory

import jakarta.servlet.http.HttpSession
import com.itmo.mrdvd.dto.Dot

trait DotHistoryModel[T]:
  def getHistory(key: T): Array[Dot]
  def addDot(dot: Dot, key: T): Array[Dot]
