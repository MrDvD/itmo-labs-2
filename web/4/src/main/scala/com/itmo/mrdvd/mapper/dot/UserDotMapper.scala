package com.itmo.mrdvd.mapper.dot

import java.sql.ResultSet
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper

class UserDotMapper
    extends Mapper[ResultSet, Entry[Entry[Int, String], DotResult]]:
  override def apply(
      rs: ResultSet
  ): Either[Error, Entry[Entry[Int, String], DotResult]] =
    Right(
      Entry[Entry[Int, String], DotResult](
        Entry[Int, String](
          rs.getInt("creator_id"),
          rs.getString("login")
        ),
        DotResult(
          Dot(rs.getDouble("x"), rs.getDouble("y"), rs.getDouble("r")),
          rs.getBoolean("hit"),
          rs.getString("date")
        )
      )
    )
