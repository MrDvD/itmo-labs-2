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
  override protected def doGet(req: HttpServletRequest, resp: HttpServletResponse): Unit = 
    req.getRequestDispatcher("index.jsp").forward(req, resp)