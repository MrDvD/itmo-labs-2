package com.itmo.mrdvd.bean

import java.lang.Double

trait CoordsRange:
  def getMin: java.util.Map[String, Double]
  def getMax: java.util.Map[String, Double]
  def getStep: java.util.Map[String, Double]
