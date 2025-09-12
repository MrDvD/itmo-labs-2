package com.itmo.mrdvd.servlets

import jakarta.servlet.http.HttpServlet
import jakarta.servlet.annotation.WebServlet
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import java.io.PrintWriter

@WebServlet(
  name = "ControllerServlet",
  description = "Delegates the HTTP request to other components",
  urlPatterns = Array("/")
)
class ControllerServlet extends HttpServlet:
  private val msg: String = "Привет от ControllerServlet"

  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit = 
    resp.setContentType("text/html")
    val out = resp.getWriter()
    out.println("<h1>" + msg + "</h1>")