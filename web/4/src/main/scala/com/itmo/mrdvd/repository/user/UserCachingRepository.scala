package com.itmo.mrdvd.repository.user

import com.itmo.mrdvd.repository.CachingGroupRepository
import com.itmo.mrdvd.dto.NewUser
import com.itmo.mrdvd.dto.StoredUser
import scala.util.Try
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.repository.GenericRepository
import scala.util.Success
import scala.util.Failure
import zio.ZIO

class UserCachingRepository(
    repo: GenericRepository[NewUser, StoredUser, String]
) extends CachingRepository[NewUser, StoredUser, String]:
  private var cache: Map[String, StoredUser] = repo.getAll

  override def create(obj: NewUser): Try[StoredUser] =
    val user = repo.create(obj)
    user match
      case Success(value) =>
        cache = cache + (value.login -> value)
      case Failure(err) =>
    user
  override def getAll: Map[String, StoredUser] = cache
  override def setCache(map: Map[String, StoredUser]): Unit = cache = map
  override def get(login: String): Try[StoredUser] =
    Try(cache.get(login).get)
  override def remove(login: String): Unit =
    repo.remove(login)
    cache = cache.removed(login)
