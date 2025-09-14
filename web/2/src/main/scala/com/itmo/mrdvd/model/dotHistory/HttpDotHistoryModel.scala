package com.itmo.mrdvd.model.dotHistory

import jakarta.servlet.http.HttpSession
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.AreaResult

class HttpDotHistoryModel(protected val dotHistoryKey: String) extends DotHistoryModel[HttpSession]:
  override def getHistory(session: HttpSession): Array[AreaResult] = 
    var rawDotHistory = session.getAttribute(this.dotHistoryKey)
    if rawDotHistory == null then
      rawDotHistory = Array[AreaResult]()
      session.setAttribute(this.dotHistoryKey, rawDotHistory)
    rawDotHistory match
      case dotHistory: Array[AreaResult] =>
        return dotHistory
      case _ =>
        throw RuntimeException("History retrieval error")
  override def addEntry(entry: AreaResult, session: HttpSession): Array[AreaResult] = 
    var rawDotHistory = session.getAttribute(this.dotHistoryKey)
    if rawDotHistory == null then
      val dotHistory = Array[AreaResult](entry)
      session.setAttribute(this.dotHistoryKey, dotHistory)
      return dotHistory
    rawDotHistory match
      case dotHistory: Array[AreaResult] =>
        val updatedDotHistoryBuffer = dotHistory.toBuffer
        updatedDotHistoryBuffer += entry
        val updatedDotHistory = updatedDotHistoryBuffer.toArray
        session.setAttribute(this.dotHistoryKey, updatedDotHistory)
        return updatedDotHistory
      case _ =>
        throw RuntimeException("History retrieval error")