package com.itmo.mrdvd.repository

import scala.util.Try
import com.itmo.mrdvd.dto.Page

trait PagedGroupRepository[In, Out, GroupId]:
  def create(id: GroupId, obj: In): Try[Out]
  def getGroupPage(groupId: GroupId, page: Int, pageSize: Int): Try[Page[Out]]
  def getAllGroupPages(
      groupId: GroupId,
      pageSize: Int
  ): Iterator[Try[Page[Out]]]
  def clearGroup(id: GroupId): Unit
