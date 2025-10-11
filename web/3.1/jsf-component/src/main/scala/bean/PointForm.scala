import jakarta.inject.{Named, Inject};
import jakarta.enterprise.context.SessionScoped
import com.itmo.mrdvd.repository.CachingRepository
import com.itmo.mrdvd.dto.{DotResult, Dot}
import com.itmo.mrdvd.mapper.Mapper
import java.lang.Double
import scala.util.{Success, Failure}
import com.itmo.mrdvd.bean.DotAvaliableRange
import com.itmo.mrdvd.bean.DotCoords
import com.itmo.mrdvd.event.PointResultEvent
import jakarta.faces.component.UINamingContainer
import jakarta.faces.context.FacesContext

@Named
@SessionScoped
class PointForm extends UINamingContainer, Serializable:
  @Inject @Named("cachingRepository") private var dotRepository
      : CachingRepository[DotResult, DotResult] = null
  @Inject private var dotResultMapper: Mapper[Dot, DotResult] = null
  @Inject protected var range: DotAvaliableRange = null

  def getRange(): DotAvaliableRange = range

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
  def clear(): Unit =
    dotRepository.clearAll()
