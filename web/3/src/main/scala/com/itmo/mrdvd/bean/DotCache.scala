package com.itmo.mrdvd.bean

import jakarta.inject.Named
import jakarta.enterprise.context.ApplicationScoped
import com.itmo.mrdvd.dto.DotResult
import com.itmo.mrdvd.dto.Dot

@Named("dotCache")
@ApplicationScoped
class DotCache:
  private val cache: Array[DotResult] = Array(
    DotResult(Dot(1.3, 2.1, 3.2), true, "whenever")
  )

  def getCache(): Array[DotResult] = cache

  def sendDotForm(): Unit =
    return
  
  def sendDotPlot(): Unit =
    return