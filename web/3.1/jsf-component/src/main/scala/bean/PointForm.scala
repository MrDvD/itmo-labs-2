import jakarta.inject.{Named, Inject};
import jakarta.enterprise.context.SessionScoped
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto.{DotResult, Dot}
import com.itmo.mrdvd.mapper.Mapper
import java.lang.Double
import scala.util.{Success, Failure}
import jakarta.faces.component.UINamingContainer
import jakarta.faces.context.FacesContext
import jakarta.faces.event.ComponentSystemEvent
import jakarta.faces.component.FacesComponent
import java.util.logging.Logger
import jakarta.faces.application.FacesMessage
import jakarta.enterprise.inject.spi.CDI
import jakarta.enterprise.util.AnnotationLiteral
import jakarta.enterprise.inject.literal.NamedLiteral
import jakarta.enterprise.context.ApplicationScoped
import jakarta.enterprise.util.TypeLiteral
import jakarta.enterprise.event.Event
import com.itmo.mrdvd.dto.PointResultEvent
import com.itmo.mrdvd.dto.ClearPointsEvent

@FacesComponent
class PointForm extends UINamingContainer, Serializable:
  private lazy val dotRepository = CDI
    .current()
    .select(
      new TypeLiteral[CachingRepository[DotResult, DotResult]] {},
      NamedLiteral.of("cachingRepository")
    )
    .get()
  private lazy val dotResultMapper =
    CDI.current().select(new TypeLiteral[Mapper[Dot, DotResult]] {}).get()
  private val pointResultEvent = CDI
    .current()
    .select(new TypeLiteral[Event[PointResultEvent[DotResult]]] {})
    .get()
  private val clearPointsEvent = CDI
    .current()
    .select(new TypeLiteral[Event[ClearPointsEvent]] {})
    .get()
  private val allowedInputTypes = Set("text", "slider")
  private val inputFieldNames = Seq("inputTypeX", "inputTypeY", "inputTypeR")

  def send(x: Double, y: Double, r: Double): Unit =
    dotResultMapper(Dot(x, y, r)) match
      case Right(value) =>
        throw value
      case Left(value) =>
        dotRepository.create(value) match
          case Failure(exception) =>
            throw exception
          case Success(value) =>
            pointResultEvent.fire(PointResultEvent(value))
  def validateInputTypes(): Unit =
    for (inputName <- inputFieldNames)
      val input = getAttributes().get(inputName).asInstanceOf[String]
      if !allowedInputTypes.contains(input) then
        throw Error(
          f"Unknown input type \"$input\" specified for attribute $inputName."
        )
  def clear(): Unit =
    dotRepository.clearAll
    clearPointsEvent.fire(ClearPointsEvent())
