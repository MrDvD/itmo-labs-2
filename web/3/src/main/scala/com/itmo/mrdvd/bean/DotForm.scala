package com.itmo.mrdvd.bean

import java.lang.Double
import jakarta.inject.Named;
import jakarta.inject.Inject
import jakarta.enterprise.context.SessionScoped

@Named
@SessionScoped
class DotForm extends Serializable:
  @Inject private var range: DotAvaliableRange = null
  @Inject private var keys: DotInput = null
  @Inject private var plot: DotInput = null
  private var scale: Double = 0
  
  def getRange(): DotAvaliableRange = range
  def getKeys(): DotInput = keys
  def getPlot(): DotInput = plot

  def getR(): Double = keys.getR()
  def setR(r: Double): Unit =
    keys.setR(r)
    plot.setR(r)
  
  def getScale(): Double = scale
  def setScale(newScale: Double) = scale = newScale