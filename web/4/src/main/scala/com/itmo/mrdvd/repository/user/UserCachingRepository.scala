package com.itmo.mrdvd.repository.user

import com.itmo.mrdvd.repository.CachingGroupRepository
import com.itmo.mrdvd.dto._
import scala.util.Try
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.repository.GenericRepository
import scala.util.Success
import scala.util.Failure
import zio.ZIO

class UserCachingRepository(
    repo: GenericRepository[User, Entry[Int, User], String]
) extends CachingRepository[User, Entry[Int, User], String]:
  private var cache: Map[String, Entry[Int, User]] = repo.getAll

  override def create(obj: User): Try[Entry[Int, User]] =
    val user = repo.create(obj)
    user match
      case Success(created) =>
        setCache(cache.updated(created.value.login, created))
      case Failure(err) =>
    user
  override def getAll: Map[String, Entry[Int, User]] = cache
  override def setCache(map: Map[String, Entry[Int, User]]): Unit = cache = map
  override def get(login: String): Try[Entry[Int, User]] =
    Try(cache.get(login).get)
  override def remove(login: String): Unit =
    repo.remove(login)
    cache = cache.removed(login)
