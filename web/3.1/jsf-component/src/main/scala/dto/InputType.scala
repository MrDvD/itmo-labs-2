package com.itmo.mrdvd.dto

enum InputType(name: String):
  case Text extends InputType("text")
  case Slider extends InputType("slider")
