package com.itmo.mrdvd.repository

import com.itmo.mrdvd.dto.DotResult
import java.sql.{Connection, DriverManager}
import scala.util.{Try, Using, Success, Failure}
import com.itmo.mrdvd.mapper.ResultSetMapper
import java.sql.ResultSet
import scala.annotation.tailrec

class DotResultJdbcRepository extends GenericRepository[DotResult, DotResult]:
  protected var rsMapper: ResultSetMapper = null
  private val sqlCreate =
    "insert into DOTS (x, y, r, hit, date) values (?, ?, ?, ?, ?)"
  private val sqlGetAll = "select x, y, r, hit, date from DOTS"
  private val sqlClearAll = "truncate DOTS cascade"

  @tailrec
  private def readDots(
      rs: ResultSet,
      dotArray: Array[DotResult]
  ): Array[DotResult] =
    if !rs.next() then dotArray
    else
      rsMapper(rs) match
        case Left(value)  => readDots(rs, value +: dotArray)
        case Right(value) =>
          throw Error("Database selection error")
  override def create(dot: DotResult): Try[DotResult] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(sqlCreate))
      stmt.setDouble(1, dot.dot.X)
      stmt.setDouble(2, dot.dot.Y)
      stmt.setDouble(3, dot.dot.R)
      stmt.setBoolean(4, dot.hit)
      stmt.setString(5, dot.date)
      if stmt.executeUpdate() > 0 then dot
      else throw Error("Database insertion error")
    )
  override def getAll: Array[DotResult] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt = use(conn.createStatement())
        val rs = use(stmt.executeQuery(sqlGetAll))
        readDots(rs, Array[DotResult]())
      )
      .get
  override def clearAll: Unit =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.createStatement())
      stmt.executeUpdate(sqlClearAll)
    )

object JdbcConnector:
  val getEnv = (envVar: String) =>
    () =>
      val rawVar = sys.env.get(envVar)
      if rawVar.isEmpty then
        throw Error(s"Environment variable ${envVar} is not found.")
      rawVar.get
  val dbHost = getEnv("POSTGRES_HOST")
  val dbName = getEnv("POSTGRES_DB")
  val jdbcUrl = s"jdbc:postgresql://${dbHost()}:5432/${dbName()}"
  val dbUsername = getEnv("POSTGRES_USER")
  val dbPassword = getEnv("POSTGRES_PASSWORD")

  def getConnection: Connection =
    DriverManager.getConnection(jdbcUrl, dbUsername(), dbPassword())
