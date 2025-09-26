package com.itmo.mrdvd.bean

import jakarta.inject.Named
import jakarta.enterprise.context.ApplicationScoped
import com.itmo.mrdvd.dto.DotResult
import com.itmo.mrdvd.dto.Dot
import jakarta.inject.Inject
import com.itmo.mrdvd.service.dotArea.DotAreaService
import scala.math.BigDecimal.RoundingMode

@Named
@ApplicationScoped
class DotCache:
  @Inject private var dotAreaService: DotAreaService = null
  @Inject private var form: DotForm = null
  private var cache: Array[DotResult] = Array()

  def getCache(): Array[DotResult] = cache
  def sendKeys(): Unit =
    val keys = form.getKeys()
    cache :+= dotAreaService.addDot(Dot(keys.getX(), keys.getY(), form.getR()))
  def sendPlot(): Unit =
    var plot = form.getPlot()
    cache :+= dotAreaService.addDot(Dot(
      BigDecimal.valueOf(plot.getX() * form.getR()).setScale(2, RoundingMode.HALF_UP).doubleValue,
      BigDecimal.valueOf(plot.getY() * form.getR()).setScale(2, RoundingMode.HALF_UP).doubleValue,
      form.getR()
      )
    )