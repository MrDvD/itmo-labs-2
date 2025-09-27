package com.itmo.mrdvd.bean

import java.lang.Double
import jakarta.inject.{Named, Inject};
import jakarta.enterprise.context.SessionScoped
import com.itmo.mrdvd.dto.{Dot, DotResult}
import com.itmo.mrdvd.mapper.Mapper
import scala.math.BigDecimal.RoundingMode
import com.itmo.mrdvd.repository.CachingRepository
import scala.util.Failure
import scala.util.Success

@Named
@SessionScoped
class DotForm extends Serializable:
  @Inject @Named("cachingRepository") private var dotRepository
      : CachingRepository[DotResult, DotResult] = null
  @Inject private var dotResultMapper: Mapper[Dot, DotResult] = null
  @Inject protected var range: DotAvaliableRange = null
  @Inject protected var keys: DotCoords = null
  @Inject protected var plot: DotCoords = null
  private var scale: Double = null
  private var r: Double = null

  def getRange(): DotAvaliableRange = range
  def getCache(): Array[DotResult] = dotRepository.getAll()
  def getKeys(): DotCoords = keys
  def getPlot(): DotCoords = plot

  def getR(): Double = r
  def setR(R: Double): Unit = r = R

  def getScale(): Double = scale
  def setScale(newScale: Double) = scale = newScale

  def sendKeys(): Unit =
    dotResultMapper(Dot(keys.getX(), keys.getY(), r)) match
      case Right(value) =>
        throw value
      case Left(value) =>
        dotRepository.create(value) match
          case Failure(exception) =>
            throw exception
          case Success(value) =>
            return

  def sendPlot(): Unit =
    dotResultMapper(
      Dot(
        BigDecimal
          .valueOf(plot.getX() * r)
          .setScale(2, RoundingMode.HALF_UP)
          .doubleValue,
        BigDecimal
          .valueOf(plot.getY() * r)
          .setScale(2, RoundingMode.HALF_UP)
          .doubleValue,
        r
      )
    ) match
      case Right(value) =>
        throw value
      case Left(value) =>
        dotRepository.create(value) match
          case Failure(exception) =>
            throw exception
          case Success(value) =>
            return
