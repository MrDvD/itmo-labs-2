package com.itmo.mrdvd.mapper

import java.sql.ResultSet
import com.itmo.mrdvd.dto.{Dot, DotResult}

class ResultSetMapper extends Mapper[ResultSet, DotResult]:
  override def apply(rs: ResultSet): Either[DotResult, Error] =
    Left(
      DotResult(
        Dot(rs.getDouble("x"), rs.getDouble("y"), rs.getDouble("r")),
        rs.getBoolean("hit"),
        rs.getString("date")
      )
    )
