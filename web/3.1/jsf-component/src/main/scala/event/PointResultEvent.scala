package com.itmo.mrdvd.event

import jakarta.faces.event.ComponentSystemEvent
import jakarta.faces.component.UIComponent

class PointResultEvent[T](component: UIComponent, result: T)
    extends ComponentSystemEvent(component)
