module lab_types
  type :: interval
    real :: left, right
  end type interval
end module lab_types

module lab_functions
  use lab_types
  implicit none

  real, parameter :: PI = 3.1415926
  
contains
  real function compute_velocity(m_this, m_other, V, coeff)
    real, intent(in) :: m_this, m_other, V, coeff
    compute_velocity = V * sqrt(m_other / m_this * coeff / 2)
  end function compute_velocity

  real function compute_max_theta(v, V_SYS)
    real, intent(in) :: v, V_SYS
    if (V_SYS < v) then
      compute_max_theta = PI
    else
      compute_max_theta = asin(v / V_SYS)
    end if
  end function compute_max_theta

  function compute_interval(v, V_SYS) result(res)
    real, intent(in) :: v, V_SYS
    type(interval) :: res
    res%left = abs(v - V_SYS)
    res%right = v + V_SYS
  end function compute_interval

  real function compute_theta_0(theta, v, V_SYS)
    real, intent(in) :: theta, v, V_SYS
    compute_theta_0 = theta + asin(V_SYS / v * sin(theta))
  end function compute_theta_0

  real function get_real(msg)
    character(len=*), intent(in) :: msg
    write(*,'(A,1X)',advance='no') trim(msg)
    read*, get_real
  end function get_real

  real function compute_new_velocity(v_mag, V_sys, theta)
    real, intent(in) :: v_mag, V_sys, theta
    compute_new_velocity = sqrt(v_mag**2 + V_sys**2 + 2.0 * v_mag * V_sys * cos(theta))
  end function compute_new_velocity

  subroutine draw_circle(v)
    real, intent(in) :: v
    integer :: i
    real :: angle, x, y
    call pgslw(1)
    call pgsls(2)
    do i = 0, 360
      angle = real(i) * PI / 180.0
      x = v * cos(angle)
      y = v * sin(angle)
      if (i == 0) then
        call pgmove(x, y)
      else
        call pgdraw(x, y)
      end if
    end do
  end subroutine draw_circle

  subroutine draw_tangent(x0, y0, v, theta_max)
    real, intent(in) :: x0, y0, v, theta_max
    real :: x_tan, y_tan
    if (theta_max >= PI - 0.001) return
    call pgsls(3)

    x_tan = x0 + v * cos(theta_max)
    y_tan = y0 + v * sin(theta_max)
    call pgmove(x0, y0)
    call pgdraw(x_tan, y_tan)

    y_tan = y0 + v * sin(-theta_max)
    call pgmove(x0, y0)
    call pgdraw(x_tan, y_tan)
    call pgsls(1)
  end subroutine draw_tangent

  subroutine draw_plot_panel(panel_idx, v_mag, V_sys, theta_max, current_phi, label)
    integer, intent(in) :: panel_idx
    real, intent(in) :: v_mag, V_sys, theta_max, current_phi
    character(len=*), intent(in) :: label
    
    real :: plot_max, theta_0_val
    character(len=32) :: theta_str, theta0_str, vel_str
    
    theta_0_val = compute_theta_0(current_phi, v_mag, V_sys)
    
    plot_max = max(v_mag, V_sys) * 1.5
    call pgpanl(panel_idx, 1)
    call pgbbuf()
    call pgeras() 
    call pgwnad(-plot_max, plot_max, -plot_max, plot_max)
    call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    call pglab('X', 'Y', label)
    
    call draw_circle(v_mag)

    call pgpt(1, 0.0, 0.0, 17)
    call pgpt(1, -V_sys, 0.0, 17)
    call pgptxt(-V_sys, 0.15, 0.0, 0.0, 'A')
    call pgsci(1)
    call pgarro(-V_sys, 0.0, 0.0, 0.0)
    
    call draw_tangent(-V_sys, 0.0, V_sys, theta_max)

    call pgslw(3)
    call pgsci(2) ! red color
    call pgarro(-V_sys, 0.0, v_mag * cos(theta_0_val), v_mag * sin(theta_0_val))
    call pgsls(2)
    call pgsci(1)
    call pgarro(0.0, 0.0, v_mag * cos(theta_0_val), v_mag * sin(theta_0_val))
    
    ! legend
    call pgsci(1)
    call pgslw(1)
    call pgsls(1)
    
    write(theta_str, '(A, F0.2, A)') '\gh = ', current_phi, ' rad'
    write(theta0_str, '(A, F0.2, A)') '\gh\d0\u = ', theta_0_val, ' rad'
    write(vel_str, '(A, F0.2, A)') 'v_new = ', compute_new_velocity(v_mag, V_sys, theta_0_val), ' m/s'
    
    call pgmtxt('T', -1.5, 0.02, 0.0, theta_str)
    call pgmtxt('T', -3.0, 0.02, 0.0, theta0_str)
    call pgmtxt('T', -4.5, 0.02, 0.0, vel_str)
    
    call pgebuf()
  end subroutine draw_plot_panel

  subroutine handle_interaction(v1, v2, V_sys, th1, th2, m1, m2)
    real, intent(in) :: v1, v2, V_sys, th1, th2, m1, m2
    real :: phi1, phi2, cx, cy, ratio
    integer :: n = 50
    character :: ch
    logical :: looping
    character(len=50) :: title1, title2

    looping = .true.

    write(*,*) "--- Interactive mode ---"
    write(*,*) "  'a' - Rotate CCW"
    write(*,*) "  'd' - Rotate CW"
    write(*,*) "  'q' - Quit"

    do while (looping)
      ratio = (real(n) / 50.0) - 1.0
      phi1 = th1 * ratio
      phi2 = th2 * ratio

      write(title1, '(A, F0.2, A)') 'Body 1 (m = ', m1, ')'
      write(title2, '(A, F0.2, A)') 'Body 2 (m = ', m2, ')'
      
      call draw_plot_panel(1, v1, V_sys, th1, phi1, title1)
      call draw_plot_panel(2, v2, V_sys, th2, phi2, title2)
      
      call pgcurs(cx, cy, ch)
      
      select case (ch)
      case ('a', 'A')
        if (n + 1 < 100) then
          n = n + 1
        end if
      case ('d', 'D')
        if (n - 1 > 0) then
          n = n - 1
        end if
      case ('q', 'Q')
        looping = .false.
      end select
    end do
  end subroutine handle_interaction
end module lab_functions

program lab_6
  use lab_functions
  use lab_types
  implicit none
  real :: m1, m2, V, percent
  real :: v1, v2, theta1, theta2
  type(interval) :: interval1, interval2

  real :: ier
  integer :: pgopen

  ! input data
  do
    m1 = get_real('m1:')
    if (m1 <= 0) then
      write(0,'(A)') "[err] Mass must be positive."
    else
      exit
    end if
  end do
  do
    m2 = get_real('m2:')
    if (m2 <= 0) then
      write(0,'(A)') "[err] Mass must be positive."
    else
      exit
    end if
  end do
  do
    V = get_real('V:')
    if (V <= 0) then
      write(0,'(A)') "[err] Velocity must be positive."
    else
      exit
    end if
  end do
  do
    percent = get_real('percent:')
    if (percent <= 0) then
      write(0,'(A)') "[err] Percentage must be positive."
    else
      exit
    end if
  end do

  v1 = compute_velocity(m1, m2, V, percent / 100)
  v2 = compute_velocity(m2, m1, V, percent / 100)

  theta1 = compute_max_theta(v1, V)
  theta2 = compute_max_theta(v2, V)

  interval1 = compute_interval(v1, V)
  interval2 = compute_interval(v2, V)

  write(*,*) "--- Theoretical calculation ---"
  write(*,*) "v1:", v1
  write(*,*) "v2:", v2
  write(*,*) "theta1:", theta1
  write(*,*) "theta2:", theta2
  write(*,*) "v1_left:", interval1%left
  write(*,*) "v1_right:", interval1%right
  write(*,*) "v2_left:", interval2%left
  write(*,*) "v2_right:", interval2%right

  ! PGPLOT
  ier = pgopen('/XSERVE')
  if (ier .le. 0) stop "Could not open PGPLOT device."

  call pgpap(18.0, 0.5)
  
  call pgask(.false.)
  call pgscr(0, 1.0, 1.0, 1.0)
  call pgscr(1, 0.0, 0.0, 0.0)
  call pgsubp(2, 1)

  call handle_interaction(v1, v2, V, theta1, theta2, m1, m2)

  call pgend()
end program lab_6