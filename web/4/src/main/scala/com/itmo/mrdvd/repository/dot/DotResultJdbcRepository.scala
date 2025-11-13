package com.itmo.mrdvd.repository.dot

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Using, Success, Failure}
import java.sql.ResultSet
import scala.annotation.tailrec
import com.itmo.mrdvd.mapper.Mapper
import java.sql.Statement
import com.itmo.mrdvd.dto.UserDotBinding
import com.itmo.mrdvd.repository.JdbcConnector
import com.itmo.mrdvd.repository.GroupedRepository

class DotResultJdbcRepository(
    private val rsMapper: Mapper[ResultSet, UserDotBinding]
) extends GroupedRepository[DotResult, DotResult, Int]:
  @tailrec
  private def readDotsMap(
      rs: ResultSet,
      dotMap: Map[Int, Array[DotResult]]
  ): Map[Int, Array[DotResult]] =
    if !rs.next() then dotMap
    else
      rsMapper(rs) match
        case Right(value) =>
          val rawDotArray = dotMap.get(value.userId)
          var dotArray: Array[DotResult] = null
          if dotArray.isEmpty then dotArray = Array()
          else dotArray = rawDotArray.get
          dotArray = value.dotResult +: dotArray
          readDotsMap(rs, dotMap + (value.userId -> dotArray))
        case Left(value) =>
          throw Error("Database selection error")
  @tailrec
  private def readDotsArray(
      rs: ResultSet,
      dotArray: Array[DotResult]
  ): Array[DotResult] =
    if !rs.next() then dotArray
    else
      rsMapper(rs) match
        case Right(value) => readDotsArray(rs, value.dotResult +: dotArray)
        case Left(value)  =>
          throw Error("Database selection error")
  override def create(id: Int, dot: DotResult): Try[DotResult] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      conn.setAutoCommit(false)
      val stmt = use(
        conn.prepareStatement(
          DotResultJdbcRepository.sqlCreate,
          Statement.RETURN_GENERATED_KEYS
        )
      )
      stmt.setDouble(1, dot.dot.X)
      stmt.setDouble(2, dot.dot.Y)
      stmt.setDouble(3, dot.dot.R)
      stmt.setBoolean(4, dot.hit)
      stmt.setString(5, dot.date)
      if stmt.execute() then
        val generatedKeys = use(stmt.getGeneratedKeys())
        if generatedKeys.next() then
          val dotId = generatedKeys.getInt(1)
          val manyStmt =
            use(conn.prepareStatement(DotResultJdbcRepository.sqlCreateNext))
          manyStmt.setInt(1, id)
          manyStmt.setInt(2, dotId)
          if stmt.execute() then
            conn.commit()
            Success(dot)
      conn.rollback()
      throw Error("Database insertion error")
    )
  override def getAll: Map[Int, Array[DotResult]] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt = use(conn.createStatement())
        val rs = use(stmt.executeQuery(DotResultJdbcRepository.sqlGetAll))
        readDotsMap(rs, Map())
      )
      .get
  override def getGroup(id: Int): Try[Array[DotResult]] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt =
          use(conn.prepareStatement(DotResultJdbcRepository.sqlGetGroup))
        stmt.setInt(1, id)
        val rs = use(stmt.executeQuery())
        readDotsArray(rs, Array())
      )
  override def clearGroup(id: Int): Unit =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt =
          use(conn.prepareStatement(DotResultJdbcRepository.sqlClearGroup))
        stmt.setInt(1, id)
        stmt.execute()
      )

object DotResultJdbcRepository:
  val sqlCreate =
    "insert into DOTS (x, y, r, hit, date) values (?, ?, ?, ?, ?)"
  val sqlCreateNext =
    "insert into USERS_TO_DOTS (user_id, dot_id) values (?, ?)"
  val sqlGetAll = "select x, y, r, hit, date from DOTS"
  val sqlGetGroup =
    "select x, y, r, hit, date from DOTS d join USERS_TO_DOTS u on d.id = u.dot_id where u.user_id = ?"
  val sqlClearGroup =
    "delete from DOTS d join USERS_TO_DOTS u on d.id = u.dot_id where u.user_id = ?"
