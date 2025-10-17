package com.itmo.mrdvd.listener

import jakarta.enterprise.context.ApplicationScoped
import jakarta.enterprise.event.Observes
import com.itmo.mrdvd.dto.DotResult
import jakarta.faces.context.FacesContext
import java.util.logging.Logger
import com.itmo.mrdvd.dto.PointResultEvent
import com.itmo.mrdvd.dto.ClearPointsEvent

@ApplicationScoped
class FormListener:
  val idsToUpdate = Seq("plot-area:dots", "dot-history")

  def updateDots: Unit =
    val ctx = FacesContext.getCurrentInstance()
    for (id <- idsToUpdate) do
      ctx.getPartialViewContext().getRenderIds().add(id)
  def onPointResult(@Observes event: PointResultEvent[DotResult]): Unit =
    updateDots
  def onClearPoints(@Observes event: ClearPointsEvent): Unit = updateDots
