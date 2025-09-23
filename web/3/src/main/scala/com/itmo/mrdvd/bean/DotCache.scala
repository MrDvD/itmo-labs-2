package com.itmo.mrdvd.bean

import jakarta.inject.Named
import jakarta.enterprise.context.ApplicationScoped
import com.itmo.mrdvd.dto.DotResult
import com.itmo.mrdvd.dto.Dot
import jakarta.inject.Inject

@Named("dotCache")
@ApplicationScoped
class DotCache:
  private var cache: Array[DotResult] = Array()
  @Inject @Named("dotInput") var dotInput: DotInput = null

  def getCache(): Array[DotResult] = cache

  def sendDotForm(): Unit =
    cache :+= DotResult(dotInput.getDot(), true, "testdate")
  
  def sendDotPlot(): Unit =
    return