package com.itmo.mrdvd.repository.user

import com.itmo.mrdvd.dto._
import scala.util.Try
import scala.util.Using
import com.itmo.mrdvd.repository._
import com.itmo.mrdvd.mapper.Mapper
import java.sql.ResultSet
import scala.annotation.tailrec

class UserJdbcRepository(rsMapper: Mapper[ResultSet, StoredUser])
    extends GenericRepository[NewUser, StoredUser, String]:
  @tailrec
  private def readUsers(
      rs: ResultSet,
      users: Map[String, StoredUser]
  ): Map[String, StoredUser] =
    if !rs.next() then users
    else
      rsMapper(rs) match
        case Right(value) => readUsers(rs, users + (value.login -> value))
        case Left(value)  => throw Error("Database selection error")
  override def getAll: Map[String, StoredUser] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlGetAll))
        val rs = use(stmt.executeQuery())
        readUsers(rs, Map())
      )
      .getOrElse(Map.empty)
  override def create(obj: NewUser): Try[StoredUser] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlCreate))
      stmt.setString(1, obj.login)
      stmt.setString(2, obj.password)
      if stmt.executeUpdate() > 0 then StoredUser(0, obj.login, obj.password)
      throw Error("Database insertion error")
    )
  override def get(login: String): Try[StoredUser] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlGet))
      stmt.setString(1, login)
      val rs = use(stmt.executeQuery())
      if rs.next() then rsMapper(rs)
      throw Error("Did not find a user with this login")
    )
  override def remove(login: String): Unit =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlRemove))
      stmt.setString(1, login)
      stmt.executeUpdate()
    )

object UserJdbcRepository:
  val sqlCreate =
    "insert into USERS (login, password_hash) values (?, ?)"
  val sqlGet = "select id, login, password_hash from USERS where login = ?"
  val sqlGetAll = "select id, login, password from USERS"
  val sqlRemove = "delete from USERS where login = ?"
