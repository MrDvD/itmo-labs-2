package com.itmo.mrdvd.repository

import java.sql.{Connection, DriverManager}
import com.itmo.mrdvd.AppUtils

object JdbcConnector:
  val dbHost = AppUtils.getEnv("POSTGRES_HOST")
  val dbName = AppUtils.getEnv("POSTGRES_DB")
  val jdbcUrl = s"jdbc:postgresql://${dbHost()}:5432/${dbName()}"
  val dbUsername = AppUtils.getEnv("POSTGRES_USER")
  val dbPassword = AppUtils.getEnv("POSTGRES_PASSWORD")

  def getConnection: Connection =
    DriverManager.getConnection(jdbcUrl, dbUsername(), dbPassword())
