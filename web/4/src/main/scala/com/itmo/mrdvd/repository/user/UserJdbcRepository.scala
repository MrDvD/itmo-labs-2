package com.itmo.mrdvd.repository.user

import com.itmo.mrdvd.dto._
import scala.util.Try
import scala.util.Using
import com.itmo.mrdvd.repository.JdbcConnector
import com.itmo.mrdvd.repository.GenericRepository

class UserJdbcRepository extends GenericRepository[NewUser, StoredUser, Int]:
  override def create(obj: NewUser): Try[StoredUser] =
    Using.Manager(use =>
      val conn = use(JdbcConnector.getConnection)
      val stmt = use(conn.prepareStatement(UserJdbcRepository.sqlCreate))
      stmt.setString(1, obj.login)
      stmt.setString(2, obj.password)
      if stmt.executeUpdate() > 0 then StoredUser(0, obj.login, obj.password)
      else throw Error("Database insertion error")
    )
  override def get(id: Int): Try[StoredUser] = ???
  override def remove(id: Int): Unit = ???

object UserJdbcRepository:
  val sqlCreate =
    "insert into USERS (login, password_hash) values (?, ?)"
  val sqlGet = "select login, password_hash from USERS where id = ?"
  val sqlRemove = "remove from USERS where id = ?"
