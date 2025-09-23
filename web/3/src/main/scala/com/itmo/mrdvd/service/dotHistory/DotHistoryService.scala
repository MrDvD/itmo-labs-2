package com.itmo.mrdvd.service.dotHistory

import com.itmo.mrdvd.dto.DotResult

trait DotHistoryService[T]:
  def getHistory(key: T): Array[DotResult]
  def addEntry(entry: DotResult, key: T): Array[DotResult]