package com.itmo.mrdvd.service.token

trait TokenService[T]:
  def getToken(obj: T): String
