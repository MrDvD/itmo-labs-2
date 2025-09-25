package com.itmo.mrdvd.bean

import jakarta.inject.Named;
import jakarta.inject.Inject
import jakarta.enterprise.context.SessionScoped

@Named
@SessionScoped
class DotForm extends Serializable:
  @Inject private var range: DotRange = null
  @Inject private var keys: DotInput = null
  @Inject private var plot: DotInput = null
  
  def getRange(): DotRange = range
  def getKeys(): DotInput = keys
  def getPlot(): DotInput = plot

  def getR(): Double = keys.getR()
  def setR(r: Double): Unit =
    keys.setR(r)
    plot.setR(r)