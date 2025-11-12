package com.itmo.mrdvd.repository

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Using, Success, Failure}
import java.sql.ResultSet
import scala.annotation.tailrec
import com.itmo.mrdvd.mapper.Mapper

class DotResultJdbcRepository(private val rsMapper: Mapper[ResultSet, DotResult])
    extends GroupedRepository[DotResult, DotResult, Int]:
  @tailrec
  private def readDots(
      rs: ResultSet,
      dotArray: Array[DotResult]
  ): Array[DotResult] =
    if !rs.next() then dotArray
    else
      rsMapper(rs) match
        case Right(value) => readDots(rs, value +: dotArray)
        case Left(value)  =>
          throw Error("Database selection error")
  override def create(dot: DotResult): Try[DotResult] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(DotResultJdbcRepository.sqlCreate))
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
        val rs = use(stmt.executeQuery(DotResultJdbcRepository.sqlGetAll))
        readDots(rs, Array[DotResult]())
      )
      .get
  override def clearAll: Unit =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.createStatement())
      stmt.executeUpdate(DotResultJdbcRepository.sqlClearAll)
    )

object DotResultJdbcRepository:
  val sqlCreate =
    "insert into DOTS (x, y, r, hit, date) values (?, ?, ?, ?, ?)"
  val sqlCreateNext = "insert into USERS_TO_DOTS (user_id, dot_id) values (?, ?)"
  val sqlGetAll = "select x, y, r, hit, date from DOTS"
  val sqlClearAll = "truncate DOTS cascade"