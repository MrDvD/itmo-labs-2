PROGRAM lab_9
  IMPLICIT NONE

  TYPE Point
    REAL :: x, y
  END TYPE Point
  
  TYPE Contour
    INTEGER :: n_points
    TYPE(Point), ALLOCATABLE :: pts(:)
  END TYPE Contour
  
  TYPE(Contour), ALLOCATABLE :: contours(:)
  
  CHARACTER(LEN=10)  :: letter_to_process
  CHARACTER(LEN=256) :: font_path, cmd
  CHARACTER(LEN=32)  :: dist_str
  REAL  :: bottom_tol, min_dist_val
  INTEGER :: num_contours, i, j, stat, current_bc
  REAL  :: y_min, y_max, x_min, x_max, center_x, center_y, dx, dy, y, x, area, total_mass, x1, y1, x2, y2

  OPEN(UNIT=5, FILE='config.txt', STATUS='OLD', IOSTAT=stat)
  IF (stat /= 0) STOP "config.txt not found"
  READ(5, '(A)') letter_to_process
  READ(5, '(A)') font_path
  READ(5, *)   bottom_tol
  READ(5, *)   min_dist_val
  CLOSE(5)

  WRITE(dist_str, '(F10.2)') min_dist_val

  cmd = 'python script.py "' // TRIM(font_path) // '" "' // &
      TRIM(letter_to_process) // '" ' // TRIM(ADJUSTL(dist_str))
  CALL EXECUTE_COMMAND_LINE(TRIM(cmd))

  OPEN(UNIT=10, FILE='glyph_data.txt', STATUS='OLD')
  READ(10, *) num_contours
  ALLOCATE(contours(num_contours))
  
  y_min = 1.0E30; y_max = 0
  x_min = 1.0E30; x_max = 0
  
  DO i = 1, num_contours
    READ(10, *) contours(i)%n_points
    ALLOCATE(contours(i)%pts(contours(i)%n_points))
    DO j = 1, contours(i)%n_points
      READ(10, *) contours(i)%pts(j)%x, contours(i)%pts(j)%y
      IF (contours(i)%pts(j)%y < y_min) THEN
        y_min = contours(i)%pts(j)%y
      END IF
      IF (contours(i)%pts(j)%y > y_max) THEN
        y_max = contours(i)%pts(j)%y
      END IF
      IF (contours(i)%pts(j)%x < x_min) THEN
        x_min = contours(i)%pts(j)%x
      END IF
      IF (contours(i)%pts(j)%x > x_max) THEN
        x_max = contours(i)%pts(j)%x
      END IF
    END DO
  END DO
  CLOSE(10)

  total_mass = 0.0
  center_x = 0.0
  center_y = 0.0

  dx = 2; dy = 2;

  DO y = y_min + dy/2.0, y_max, dy
    DO x = x_min + dx/2.0, x_max, dx
      IF (is_inside(x, y, contours)) THEN
        total_mass = total_mass + 1.0
        center_x = center_x + x
        center_y = center_y + y
      END IF
    END DO
  END DO

  center_x = center_x / total_mass
  center_y = center_y / total_mass

  OPEN(UNIT=20, FILE='letter.pde', STATUS='REPLACE')
  WRITE(20, '(A)') "TITLE 'Laser + Heated Base'"
  WRITE(20, '(A)') "DEFINITIONS"
  WRITE(20, '(A)') "  k = 3  h = 10  u_amb = 20  u_base = 200"
  WRITE(20, '(A, F12.2)') "  xc = ", center_x
  WRITE(20, '(A, F12.2)') "  yc = ", center_y
  WRITE(20, '(A)') "  Source = 1000 * exp(-((x-xc)^2 + (y-yc)^2)/40^2)"
  WRITE(20, '(A)') "VARIABLES u"
  WRITE(20, '(A)') "EQUATIONS div(k*grad(u)) + Source = 0"
  WRITE(20, '(A)') "BOUNDARIES REGION 1"

  current_bc = -1
  DO i = 1, num_contours
    WRITE(20, '(A, F12.2, A, F12.2, A)') " START(", contours(i)%pts(1)%x, ",", contours(i)%pts(1)%y, ")"
    DO j = 2, contours(i)%n_points
      CALL write_line(contours(i)%pts(j-1)%y, contours(i)%pts(j)%x, contours(i)%pts(j)%y)
    END DO
    CALL write_line(contours(i)%pts(contours(i)%n_points)%y, contours(i)%pts(1)%x, contours(i)%pts(1)%y)
    WRITE(20, '(A)') " CLOSE"
  END DO
  WRITE(20, '(A)') "PLOTS CONTOUR(u) VECTOR(k*grad(u)) END"
  CLOSE(20)

CONTAINS

  LOGICAL FUNCTION is_inside(px, py, in_conts)
    TYPE(Contour), INTENT(IN) :: in_conts(:)
    REAL, INTENT(IN) :: px, py
    INTEGER :: i, j, next_j, intersections
    REAL :: x1, y1, x2, y2
    
    intersections = 0
    
    DO i = 1, SIZE(in_conts)
      DO j = 1, in_conts(i)%n_points
        next_j = MERGE(j + 1, 1, j < in_conts(i)%n_points)
        
        x1 = in_conts(i)%pts(j)%x
        y1 = in_conts(i)%pts(j)%y
        x2 = in_conts(i)%pts(next_j)%x
        y2 = in_conts(i)%pts(next_j)%y

        IF (((y1 > py) .NEQV. (y2 > py)) .AND. &
            (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1)) THEN
          intersections = intersections + 1
        END IF
      END DO
    END DO
    
    is_inside = MOD(intersections, 2) /= 0
  END FUNCTION

  SUBROUTINE write_line(y_start, x_end, y_end)
    REAL, INTENT(IN) :: y_start, x_end, y_end
    INTEGER :: new_bc
    IF (ABS(y_start - y_min) < bottom_tol .AND. ABS(y_end - y_min) < bottom_tol) THEN
      new_bc = 0
    ELSE
      new_bc = 1
    END IF

    IF (new_bc /= current_bc) THEN
      current_bc = new_bc
      IF (current_bc == 0) WRITE(20, '(A)') "  VALUE(u) = u_base"
      IF (current_bc == 1) WRITE(20, '(A)') "  NATURAL(u) = h*(u_amb - u)"
    END IF
    WRITE(20, '(A, F12.2, A, F12.2, A)') "  LINE TO (", x_end, ",", y_end, ")"
  END SUBROUTINE
END PROGRAM lab_9