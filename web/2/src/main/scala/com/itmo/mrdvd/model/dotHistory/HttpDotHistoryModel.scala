package com.itmo.mrdvd.model.dotHistory

import jakarta.servlet.http.HttpSession
import com.itmo.mrdvd.dto.Dot

class HttpDotHistoryModel(protected val dotHistoryKey: String) extends DotHistoryModel[HttpSession]:
  override def getHistory(session: HttpSession): Array[Dot] = 
    var rawDotHistory = session.getAttribute(this.dotHistoryKey)
    if rawDotHistory == null then
      rawDotHistory = Array[Dot]()
      session.setAttribute(this.dotHistoryKey, rawDotHistory)
    rawDotHistory match
      case dotHistory: Array[Dot] =>
        return dotHistory
      case _ =>
        throw RuntimeException("History retrieval error")
  override def addDot(dot: Dot, session: HttpSession): Array[Dot] =
    var rawDotHistory = session.getAttribute(this.dotHistoryKey)
    if rawDotHistory == null then
      val dotHistory = Array[Dot](dot)
      session.setAttribute(this.dotHistoryKey, dotHistory)
      return dotHistory
    rawDotHistory match
      case dotHistory: Array[Dot] =>
        val updatedDotHistoryBuffer = dotHistory.toBuffer
        updatedDotHistoryBuffer += dot
        val updatedDotHistory = updatedDotHistoryBuffer.toArray
        session.setAttribute(this.dotHistoryKey, updatedDotHistory)
        return updatedDotHistory
      case _ =>
        throw RuntimeException("History retrieval error")