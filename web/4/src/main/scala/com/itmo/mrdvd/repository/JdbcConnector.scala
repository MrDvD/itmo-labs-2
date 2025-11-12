package com.itmo.mrdvd.repository

import java.sql.{Connection, DriverManager}

object JdbcConnector:
  val getEnv = (envVar: String) =>
    () =>
      val rawVar = sys.env.get(envVar)
      if rawVar.isEmpty then
        throw Error(s"Environment variable ${envVar} is not found.")
      rawVar.get
  val dbHost = getEnv("POSTGRES_HOST")
  val dbName = getEnv("POSTGRES_DB")
  val jdbcUrl = s"jdbc:postgresql://${dbHost()}:5432/${dbName()}"
  val dbUsername = getEnv("POSTGRES_USER")
  val dbPassword = getEnv("POSTGRES_PASSWORD")

  def getConnection: Connection =
    DriverManager.getConnection(jdbcUrl, dbUsername(), dbPassword())
