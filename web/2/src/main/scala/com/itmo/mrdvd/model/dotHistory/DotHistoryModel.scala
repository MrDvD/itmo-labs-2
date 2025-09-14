package com.itmo.mrdvd.model.dotHistory

import jakarta.servlet.http.HttpSession
import com.itmo.mrdvd.dto.AreaResult

trait DotHistoryModel[T]:
  def getHistory(key: T): Array[AreaResult]
  def addEntry(entry: AreaResult, key: T): Array[AreaResult]
