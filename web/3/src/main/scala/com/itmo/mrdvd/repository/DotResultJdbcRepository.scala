package com.itmo.mrdvd.repository

import com.itmo.mrdvd.dto.DotResult
import java.sql.{Connection, DriverManager}
import scala.util.{Try, Using, Success, Failure}
import jakarta.enterprise.context.ApplicationScoped
import jakarta.inject.{Named, Inject}
import com.itmo.mrdvd.mapper.ResultSetMapper

@Named("jdbcRepository")
@ApplicationScoped
class DotResultJdbcRepository extends GenericRepository[DotResult, DotResult]:
  @Inject private var rsMapper: ResultSetMapper = null
  private val sqlCreate = "insert into DOTS_HISTORY (x, y, r, hit, date) values (?, ?, ?, ?, ?)";
  private val sqlGetAll = "select * from DOTS_HISTORY";

  override def create(dot: DotResult): Try[DotResult] =
    Using(JdbcConnector.getConnection()) (conn =>
      Using(conn.prepareStatement(sqlCreate)) (stmt => 
        stmt.setDouble(1, dot.dot.X)
        stmt.setDouble(2, dot.dot.Y)
        stmt.setDouble(3, dot.dot.R)
        stmt.setBoolean(4, dot.hit)
        stmt.setString(5, dot.date)
        if stmt.executeUpdate() > 0 then
          Success(dot)
        else
          Failure(Error("Database insertion error"))
      ).flatten
    ).flatten
  override def getAll(): Array[DotResult] =
    var dotArray = Array[DotResult]()
    Using(JdbcConnector.getConnection()) (conn =>
      Using(conn.createStatement()) (stmt =>
        Using(stmt.executeQuery(sqlGetAll)) (rs =>
          while rs.next() do
            val dotResult = rsMapper (rs)
            dotResult match
              case Left(value) =>
                dotArray = value +: dotArray
              case Right(value) =>
                throw Error("Database selection error")
        )
      )
    )
    return dotArray

object JdbcConnector:
  val getEnv = (envVar: String) => () =>
    val rawVar = sys.env.get(envVar)
    if rawVar.isEmpty then
      throw Error(s"Environment variable ${envVar} is not found.")
    rawVar.get
  val dbHost = getEnv("POSTGRES_HOST")
  val dbName = getEnv("POSTGRES_DB")
  val jdbcUrl = s"jdbc:postgresql://${dbHost()}:5432/${dbName()}"
  val dbUsername = getEnv("POSTGRES_USER")
  val dbPassword = getEnv("POSTGRES_PASSWORD")

  def getConnection(): Connection =
    DriverManager.getConnection(jdbcUrl, dbUsername(), dbPassword())