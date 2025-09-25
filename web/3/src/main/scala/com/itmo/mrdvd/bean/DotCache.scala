package com.itmo.mrdvd.bean

import jakarta.inject.Named
import jakarta.enterprise.context.ApplicationScoped
import com.itmo.mrdvd.dto.DotResult
import com.itmo.mrdvd.dto.Dot
import jakarta.inject.Inject
import com.itmo.mrdvd.service.dotArea.DotAreaService

@Named
@ApplicationScoped
class DotCache:
  @Inject private var dotAreaService: DotAreaService = null
  @Inject private var form: DotForm = null
  private var cache: Array[DotResult] = Array()

  def getCache(): Array[DotResult] = cache
  def sendKeys(): Unit =
    cache :+= dotAreaService.addDot(form.getKeys().getDot())
  def sendPlot(): Unit =
    var normalDot = form.getPlot().getDot()
    cache :+= dotAreaService.addDot(Dot(
      normalDot.X * normalDot.R,
      normalDot.Y * normalDot.R,
      normalDot.R
      )
    )