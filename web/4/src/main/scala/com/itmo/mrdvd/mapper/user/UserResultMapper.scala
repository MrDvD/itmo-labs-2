package com.itmo.mrdvd.mapper.user

import java.sql.ResultSet
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper

class UserResultMapper extends Mapper[ResultSet, Entry[Int, User]]:
  override def apply(rs: ResultSet): Either[Error, Entry[Int, User]] =
    Right(
      Entry[Int, User](
        rs.getInt("id"),
        User(
          rs.getString("login"),
          rs.getString("password_hash")
        )
      )
    )
