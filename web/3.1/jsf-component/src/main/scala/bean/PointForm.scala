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

@FacesComponent
class PointForm extends UINamingContainer, Serializable:
  @Inject @Named("cachingRepository") private var dotRepository
      : CachingRepository[DotResult, DotResult] = null
  @Inject private var dotResultMapper: Mapper[Dot, DotResult] = null
  private val allowedInputTypes = Set("text", "slider")

  def fireResultEvent(result: DotResult): Unit =
    val context = FacesContext.getCurrentInstance
    context.getApplication.publishEvent(
      context,
      classOf[PointResultEvent[DotResult]],
      PointResultEvent[DotResult](this, result)
    )
  def send(x: Double, y: Double, r: Double): Unit =
    dotResultMapper(Dot(x, y, r)) match
      case Right(value) =>
        throw value
      case Left(value) =>
        dotRepository.create(value) match
          case Failure(exception) =>
            throw exception
          case Success(value) => fireResultEvent(value)
  def validateInputTypes(): Unit =
    for (inputName <- Seq("input_type_X", "input_type_Y", "input_type_R"))
      val input = getAttributes().get(inputName).asInstanceOf[String]
      if !allowedInputTypes.contains(input) then
        throw Error(
          f"Unknown input type \"$input\" specified for attribute $inputName."
        )
  def clear(): Unit =
    dotRepository.clearAll()
