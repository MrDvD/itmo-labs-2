package com.itmo.mrdvd.service.crypto

trait CryptoService:
  def hash(str: String): String
  def compareHash(str1: String, str2: String): Boolean
