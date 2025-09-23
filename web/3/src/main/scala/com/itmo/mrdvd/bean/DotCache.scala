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
  @Inject private var dotInput: DotInput = null
  @Inject private var dotAreaService: DotAreaService = null
  private var cache: Array[DotResult] = Array()

  def getCache(): Array[DotResult] = cache
  def sendDotForm(): Unit =
    cache :+= dotAreaService.addDot(dotInput.getDot())
  def sendDotPlot(): Unit =
    return