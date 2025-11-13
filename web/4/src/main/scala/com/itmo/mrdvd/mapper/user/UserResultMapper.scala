package com.itmo.mrdvd.mapper.user

import java.sql.ResultSet
import com.itmo.mrdvd.dto.StoredUser
import com.itmo.mrdvd.mapper.Mapper

class UserResultMapper extends Mapper[ResultSet, StoredUser]:
  override def apply(rs: ResultSet): Either[Error, StoredUser] =
    Right(
      StoredUser(
        rs.getInt("id"),
        rs.getString("login"),
        rs.getString("password_hash")
      )
    )
