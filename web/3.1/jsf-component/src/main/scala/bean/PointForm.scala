import jakarta.inject.{Named, Inject};
import jakarta.enterprise.context.SessionScoped
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto.{DotResult, Dot}
import com.itmo.mrdvd.mapper.Mapper
import java.lang.Double
import scala.util.{Success, Failure}
import com.itmo.mrdvd.bean.DotCoords
import com.itmo.mrdvd.event.PointResultEvent
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
import com.itmo.mrdvd.mapper.DotResultMapper
import com.itmo.mrdvd.repository.DotResultCachingRepository
import jakarta.enterprise.util.TypeLiteral

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
  private val allowedInputTypes = Set("text", "slider")
  private val inputFieldNames = Seq("inputTypeX", "inputTypeY", "inputTypeR")

  def fireResultEvent(result: DotResult): Unit =
    val context = FacesContext.getCurrentInstance
    context.getApplication.publishEvent(
      context,
      classOf[PointResultEvent[DotResult]],
      PointResultEvent[DotResult](this, result)
    )
  def send(x: Double, y: Double, r: Double): Unit =
    val context = FacesContext.getCurrentInstance
    context.addMessage(
      null,
      new FacesMessage(
        FacesMessage.SEVERITY_ERROR,
        "Validation Error",
        f"sending values: $x, $y, $r"
      )
    )
    dotResultMapper(Dot(x, y, r)) match
      case Right(value) =>
        throw value
      case Left(value) =>
        dotRepository.create(value) match
          case Failure(exception) =>
            throw exception
          case Success(value) => fireResultEvent(value)
  def validateInputTypes(): Unit =
    for (inputName <- inputFieldNames)
      val input = getAttributes().get(inputName).asInstanceOf[String]
      if !allowedInputTypes.contains(input) then
        throw Error(
          f"Unknown input type \"$input\" specified for attribute $inputName."
        )
  def clear(): Unit =
    dotRepository.clearAll()
