package com.itmo.mrdvd.bean

import java.lang.Double
import jakarta.inject.Named;
import jakarta.inject.Inject
import jakarta.enterprise.context.SessionScoped

@Named
@SessionScoped
class DotForm extends Serializable:
  @Inject private var range: DotAvaliableRange = null
  @Inject private var keys: DotCoords = null
  @Inject private var plot: DotCoords = null
  private var scale: Double = null
  private var r: Double = null
  
  def getRange(): DotAvaliableRange = range
  def getKeys(): DotCoords = keys
  def getPlot(): DotCoords = plot

  def getR(): Double = r
  def setR(R: Double): Unit = r = R
  
  def getScale(): Double = scale
  def setScale(newScale: Double) = scale = newScale