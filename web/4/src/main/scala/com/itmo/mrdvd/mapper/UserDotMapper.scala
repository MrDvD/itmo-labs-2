package com.itmo.mrdvd.mapper

import java.sql.ResultSet
import com.itmo.mrdvd.dto._

class UserDotMapper extends Mapper[ResultSet, UserDotBinding]:
  override def apply(rs: ResultSet): Either[Error, UserDotBinding] =
    Right(
      UserDotBinding(
        rs.getInt("user_id"),
        DotResult(
          Dot(rs.getDouble("x"), rs.getDouble("y"), rs.getDouble("r")),
          rs.getBoolean("hit"),
          rs.getString("date")
        )
      )
    )
