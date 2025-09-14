package com.itmo.mrdvd.servlet

import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServlet
import jakarta.servlet.annotation.WebServlet
import com.itmo.mrdvd.mapper.RawDotMapper
import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.model.dotHistory.HttpDotHistoryModel
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.model.dotArea.Lab2DotAreaModel

@WebServlet(
  name = "AreaCheckServlet",
  description = "Checks if a point is in the area",
  urlPatterns = Array("/AreaCheck")
)
class AreaCheckServlet extends HttpServlet:
  protected val historyModel = HttpDotHistoryModel("dots-history")
  protected val rawDotMapper = RawDotMapper() 
  protected val dotAreaModel = Lab2DotAreaModel()
  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit = 
    val rawDot = req.getAttribute("rawDot").asInstanceOf[RawDot]
    val dot = rawDotMapper.map(rawDot)
    if dot.isEmpty then
      resp.sendError(400, "Bad request")
      return
    val areaResult = dotAreaModel.addDot(dot.get)
    req.setAttribute("dots", this.historyModel.addEntry(areaResult, req.getSession()))
    req.getRequestDispatcher("components/area.jsp").forward(req, resp)