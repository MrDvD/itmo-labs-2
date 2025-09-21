package com.itmo.mrdvd.service.dotHistory

import com.itmo.mrdvd.dto.AreaResult

trait DotHistoryService[T]:
  def getHistory(key: T): Array[AreaResult]
  def addEntry(entry: AreaResult, key: T): Array[AreaResult]
