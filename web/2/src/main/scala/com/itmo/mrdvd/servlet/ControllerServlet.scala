package com.itmo.mrdvd.servlet

import jakarta.servlet.http.HttpServlet
import jakarta.servlet.annotation.WebServlet
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import java.io.PrintWriter
import com.itmo.mrdvd.dto.Dot
import com.itmo.mrdvd.dto.RawDot
import com.itmo.mrdvd.model.dotHistory.HttpDotHistoryModel

@WebServlet(
  name = "ControllerServlet",
  description = "Delegates the HTTP request to other components",
  urlPatterns = Array("/")
)
class ControllerServlet extends HttpServlet:
  protected val historyModel = HttpDotHistoryModel("dots-history")
  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit =
    val X = req.getParameter("X")
    val Y = req.getParameter("Y")
    val R = req.getParameter("R")
    if X != null && Y != null && R != null then
      req.setAttribute("rawDot", RawDot(X, Y, R))
      req.getRequestDispatcher("/AreaCheck").forward(req, resp)
    else
      req.setAttribute("dots", this.historyModel.getHistory(req.getSession()))
      req.getRequestDispatcher("main.jsp").forward(req, resp)