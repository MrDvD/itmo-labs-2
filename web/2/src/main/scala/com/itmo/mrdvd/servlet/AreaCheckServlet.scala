package com.itmo.mrdvd.servlet

import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServlet
import jakarta.servlet.annotation.WebServlet
import com.itmo.mrdvd.mapper.RawDotMapper
import com.itmo.mrdvd.validator.RawDotValidator
import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.model.dotHistory.HttpDotHistoryModel
import com.itmo.mrdvd.dto.Dot

@WebServlet(
  name = "AreaCheckServlet",
  description = "Checks if a point is in the area",
  urlPatterns = Array("/AreaCheck")
)
class AreaCheckServlet extends HttpServlet:
  protected val historyModel = HttpDotHistoryModel("dots-history")
  protected val rawDotMapper = RawDotMapper(RawDotValidator()) 
  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit = 
    val rawDot = req.getAttribute("rawDot").asInstanceOf[RawDot]
    val dot = rawDotMapper.map(rawDot)
    if dot.isEmpty then
      resp.sendError(400, "Bad request")
    else
      req.setAttribute("dots", this.historyModel.addDot(dot.get, req.getSession()))
      req.getRequestDispatcher("components/area.jsp").forward(req, resp)