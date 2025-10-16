package com.itmo.mrdvd.listener

import jakarta.enterprise.context.ApplicationScoped
import jakarta.enterprise.event.Observes
import com.itmo.mrdvd.dto.DotResult
import jakarta.faces.context.FacesContext
import java.util.logging.Logger
import com.itmo.mrdvd.dto.PointResultEvent

@ApplicationScoped
class PointResultListener:
  val idsToUpdate = Seq("plot-area:dots", "dot-history")

  def onPointResult(@Observes event: PointResultEvent[DotResult]): Unit =
    val ctx = FacesContext.getCurrentInstance()
    for (id <- idsToUpdate) do
      ctx.getPartialViewContext().getRenderIds().add(id)
