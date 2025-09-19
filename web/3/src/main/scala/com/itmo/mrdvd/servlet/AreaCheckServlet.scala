package com.itmo.mrdvd.servlet

import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServlet
import jakarta.servlet.annotation.WebServlet
import com.itmo.mrdvd.mapper.RawDotMapper
import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.service.dotHistory.HttpDotHistoryService
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.service.dotArea.Lab2DotAreaService

@WebServlet(
  name = "AreaCheckServlet",
  description = "Checks if a point is in the area",
  urlPatterns = Array("/AreaCheck")
)
class AreaCheckServlet extends HttpServlet:
  protected val historyModel = HttpDotHistoryService("dots-history")
  protected val rawDotMapper = RawDotMapper() 
  protected val dotAreaModel = Lab2DotAreaService()
  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit = 
    val rawDot = req.getAttribute("rawDot").asInstanceOf[RawDot]
    val dot = rawDotMapper.apply(rawDot)
    dot match {
      case Right(value) =>
        resp.sendError(400, value.getMessage())
      case Left(value) =>
        val areaResult = dotAreaModel.addDot(value)
        req.setAttribute("dots", historyModel.addEntry(areaResult, req.getSession()))
        req.getRequestDispatcher("components/area.jsp").forward(req, resp)
    }