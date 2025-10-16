package com.itmo.mrdvd.listener

import jakarta.enterprise.context.ApplicationScoped
import jakarta.enterprise.event.Observes
import com.itmo.mrdvd.event.PointResultEvent
import com.itmo.mrdvd.dto.DotResult
import jakarta.faces.context.FacesContext

@ApplicationScoped
class PointResultListener:
  val idsToUpdate = Seq("plot-area:dots", "dot-history")

  def onPointResult(@Observes event: PointResultEvent[DotResult]): Unit =
    val ctx = event.getFacesContext()
    for (id <- idsToUpdate) do
      ctx.getPartialViewContext().getRenderIds().add(id)
