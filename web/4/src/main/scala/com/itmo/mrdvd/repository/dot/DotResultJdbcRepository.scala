package com.itmo.mrdvd.repository.dot

import com.itmo.mrdvd.dto.DotResult
import scala.util.{Try, Using, Success, Failure}
import java.sql.ResultSet
import scala.annotation.tailrec
import com.itmo.mrdvd.mapper.Mapper
import java.sql.Statement
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.repository._
import zio.json.EncoderOps

class DotResultJdbcRepository(
    private val rsMapper: Mapper[ResultSet, Entry[Entry[Int, User], DotResult]]
) extends GroupedRepository[DotResult, Entry[String, DotResult], Int]:
  @tailrec
  private def readDotsMap(
      rs: ResultSet,
      dotMap: Map[Int, Array[Entry[String, DotResult]]] =
        Map.empty[Int, Array[Entry[String, DotResult]]]
  ): Map[Int, Array[Entry[String, DotResult]]] =
    if !rs.next() then dotMap
    else
      rsMapper(rs) match
        case Right(result) =>
          val dotArray =
            dotMap.getOrElse(
              result.key.key,
              Array.empty[Entry[String, DotResult]]
            )
          readDotsMap(
            rs,
            dotMap.updated(
              result.key.key,
              Entry[String, DotResult](
                result.key.value.login,
                result.value
              ) +: dotArray
            )
          )
        case Left(_) =>
          throw Error("Database selection error")
  @tailrec
  private def readDotsArray(
      rs: ResultSet,
      dotArray: Array[Entry[String, DotResult]] =
        Array.empty[Entry[String, DotResult]]
  ): Array[Entry[String, DotResult]] =
    if !rs.next() then dotArray
    else
      rsMapper(rs) match
        case Right(result) =>
          readDotsArray(
            rs,
            Entry[String, DotResult](
              result.key.value.login,
              result.value
            ) +: dotArray
          )
        case Left(_) =>
          throw Error("Database selection error")
  override def create(
      user_id: Int,
      dot: DotResult
  ): Try[Entry[String, DotResult]] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      conn.setAutoCommit(false)
      val stmt = use(conn.prepareStatement(DotResultJdbcRepository.sqlCreate))
      stmt.setDouble(1, dot.dot.X)
      stmt.setDouble(2, dot.dot.Y)
      stmt.setDouble(3, dot.dot.R)
      stmt.setBoolean(4, dot.hit)
      stmt.setString(5, dot.date)
      stmt.setInt(6, user_id)
      if stmt.executeUpdate <= 0 then
        conn.rollback()
        throw Error("Insertion of dot result failed")
      val otherStmt = use(
        conn.prepareStatement(
          DotResultJdbcRepository.sqlMapIdToLogin
        )
      )
      otherStmt.setInt(1, user_id)
      val rs = otherStmt.executeQuery()
      if !rs.next then
        conn.rollback()
        throw Error("Mapping of user login failed")
      Entry(
        rs.getString("login"),
        dot
      )
    )
  override def getAll: Map[Int, Array[Entry[String, DotResult]]] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt = use(conn.createStatement)
        val rs = use(stmt.executeQuery(DotResultJdbcRepository.sqlGetAll))
        readDotsMap(rs)
      )
      .get
  override def getGroup(id: Int): Try[Array[Entry[String, DotResult]]] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt =
          use(conn.prepareStatement(DotResultJdbcRepository.sqlGetGroup))
        stmt.setInt(1, id)
        val rs = use(stmt.executeQuery)
        readDotsArray(rs, Array.empty[Entry[String, DotResult]])
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
    "insert into DOTS (x, y, r, hit, date, creator_id) values (?, ?, ?, ?, ?, ?)"
  val sqlGetAll =
    "select x, y, r, hit, date, creator_id, login, password_hash from DOTS join USERS u on creator_id = u.id"
  val sqlMapIdToLogin = "select login from USERS where id = ?"
  val sqlGetGroup =
    "select x, y, r, hit, date from DOTS where creator_id = ?"
  val sqlClearGroup =
    "delete from DOTS where creator_id = ?"
