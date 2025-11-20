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
    repository: GenericRepository[User, Entry[Int, User], String]
) extends CachingRepository[User, Entry[Int, User], String]:
  private var cache: Map[String, Entry[Int, User]] =
    repository.getAll.map(user => user.value.login -> user).toMap

  override def create(obj: User): Try[Entry[Int, User]] =
    val user = repository.create(obj)
    user match
      case Success(created) =>
        setCache(cache.updated(created.value.login, created))
      case Failure(err) =>
    user
  override def getAll: Iterator[Entry[Int, User]] =
    cache.iterator.map((_, entry) => entry)
  override def setCache(map: Map[String, Entry[Int, User]]): Unit = cache = map
  override def get(login: String): Try[Entry[Int, User]] =
    Try(cache.get(login).get)
  override def remove(login: String): Unit =
    repository.remove(login)
    cache = cache.removed(login)
