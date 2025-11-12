package com.itmo.mrdvd.mapper

type Mapper[T, U] = T => Either[Error, U]
