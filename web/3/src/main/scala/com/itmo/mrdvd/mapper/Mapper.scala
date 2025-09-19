package com.itmo.mrdvd.mapper

type Mapper[T, U] = T => Either[U, Error]