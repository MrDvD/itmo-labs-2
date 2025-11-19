package com.itmo.mrdvd.mapper.dot

import java.sql.ResultSet
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper

class UserDotMapper
    extends Mapper[ResultSet, Entry[Entry[Int, User], DotResult]]:
  override def apply(
      rs: ResultSet
  ): Either[Error, Entry[Entry[Int, User], DotResult]] =
    Right(
      Entry[Entry[Int, User], DotResult](
        Entry[Int, User](
          rs.getInt("creator_id"),
          User(
            rs.getString("login"),
            rs.getString("password_hash")
          )
        ),
        DotResult(
          Dot(rs.getDouble("x"), rs.getDouble("y"), rs.getDouble("r")),
          rs.getBoolean("hit"),
          rs.getString("date")
        )
      )
    )
