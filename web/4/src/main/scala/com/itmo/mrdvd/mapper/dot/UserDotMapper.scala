package com.itmo.mrdvd.mapper.dot

import java.sql.ResultSet
import com.itmo.mrdvd.dto._
import com.itmo.mrdvd.mapper.Mapper

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
