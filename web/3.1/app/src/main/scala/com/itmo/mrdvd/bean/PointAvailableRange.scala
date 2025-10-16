package com.itmo.mrdvd.bean

import jakarta.enterprise.context.ApplicationScoped
import scala.jdk.CollectionConverters._
import jakarta.inject.Named
import java.lang.Double

@Named
@ApplicationScoped
class PointAvailableRange extends CoordsRange, Serializable:
  private val minMaxValues = Map(
    "X" -> Array(-3.0, 5.0),
    "Y" -> Array(-2.0, 2.0),
    "R" -> Array(1.0, 3.0)
  )
  override def getMin: java.util.Map[String, Double] =
    minMaxValues.view.mapValues(arr => arr(0): Double).toMap.asJava
  def getMax: java.util.Map[String, Double] =
    minMaxValues.view.mapValues(arr => arr(1): Double).toMap.asJava
