package com.itmo.mrdvd.repository.user

import com.itmo.mrdvd.dto._
import scala.util.Try
import scala.util.Using
import com.itmo.mrdvd.repository._
import com.itmo.mrdvd.mapper.Mapper
import java.sql.ResultSet
import scala.annotation.tailrec
import zio.ZIO
import java.sql.Statement

class UserJdbcRepository(rsMapper: Mapper[ResultSet, Entry[Int, User]])
    extends GenericRepository[User, Entry[Int, User], String]:
  @tailrec
  private def readUsers(
      rs: ResultSet,
      users: Map[String, Entry[Int, User]]
  ): Map[String, Entry[Int, User]] =
    if !rs.next() then users
    else
      rsMapper(rs) match
        case Right(value) => readUsers(rs, users + (value.value.login -> value))
        case Left(value)  => throw Error("Database selection error")
  override def getAll: Map[String, Entry[Int, User]] =
    Using
      .Manager(use =>
        val conn = use(JdbcConnector.getConnection)
        val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlGetAll))
        val rs = use(stmt.executeQuery())
        readUsers(rs, Map())
      )
      .getOrElse(Map.empty)
  override def create(obj: User): Try[Entry[Int, User]] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      conn.setAutoCommit(false)
      val stmt = use(
        conn.prepareStatement(
          UserJdbcRepository.sqlCreate,
          Statement.RETURN_GENERATED_KEYS
        )
      )
      stmt.setString(1, obj.login)
      stmt.setString(2, obj.password)
      if stmt.executeUpdate() <= 0 then
        conn.rollback()
        throw Error("User insertion failed")
      val generatedKeys = use(stmt.getGeneratedKeys());
      if !generatedKeys.next() then
        conn.rollback()
        throw Error("No ID generated")
      val userId = generatedKeys.getInt(1)
      conn.commit()
      Entry[Int, User](userId, obj)
    )
  override def get(login: String): Try[Entry[Int, User]] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlGet))
      stmt.setString(1, login)
      val rs = use(stmt.executeQuery())
      if rs.next() then
        rsMapper(rs) match
          case Right(value) => value
          case Left(err)    => throw err
      else throw Error("Did not find a user with this login")
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
  val sqlGetAll = "select id, login, password_hash from USERS"
  val sqlRemove = "delete from USERS where login = ?"
