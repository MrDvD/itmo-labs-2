package com.itmo.mrdvd.bean

import jakarta.enterprise.context.ApplicationScoped

@ApplicationScoped
class DotAvaliableRange extends Serializable:
  private val y = Array(-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2)
  private val r = Array(1, 1.5, 2, 2.5, 3)

  def getY(): Array[Double] = y
  def getR(): Array[Double] = r
