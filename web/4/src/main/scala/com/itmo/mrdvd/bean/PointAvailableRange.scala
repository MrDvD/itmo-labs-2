package com.itmo.mrdvd.bean

import scala.jdk.CollectionConverters._
import java.lang.Double

class PointAvailableRange extends CoordsRange, Serializable:
  private val minMaxValues = Map(
    "X" -> Array(-3.0, 5.0, 0.1),
    "Y" -> Array(-2.0, 2.0, 0.1),
    "R" -> Array(1.0, 3.0, 0.5)
  )
  override def getMin: java.util.Map[String, Double] =
    minMaxValues.view.mapValues(arr => arr(0): Double).toMap.asJava
  def getMax: java.util.Map[String, Double] =
    minMaxValues.view.mapValues(arr => arr(1): Double).toMap.asJava
  def getStep: java.util.Map[String, Double] =
    minMaxValues.view.mapValues(arr => arr(2): Double).toMap.asJava
