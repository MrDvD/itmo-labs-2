package com.itmo.mrdvd.servlets

import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServlet
import jakarta.servlet.annotation.WebServlet

@WebServlet(
  name = "AreaCheckServlet",
  description = "Checks if a point is in the area",
  urlPatterns = Array("/AreaCheck")
)
class AreaCheckServlet extends HttpServlet:
  private val msg: String = "Hello from AreaCheckServlet"

  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit = 
    resp.setContentType("text/html")
    val out = resp.getWriter()
    out.println("<h1>" + msg + "</h1>")