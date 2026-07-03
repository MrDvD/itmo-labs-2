module lab_functions
  implicit none
  real, parameter :: PI = 3.1415926
  contains

  subroutine draw_circle(xc, yc, r)
    real, intent(in) :: xc, yc, r
    integer :: i
    real :: angle, x, y
    call pgslw(3) 
    do i = 0, 360
      angle = real(i) * PI / 180.0
      x = xc + r * cos(angle)
      y = yc + r * sin(angle)
      if (i == 0) then
        call pgmove(x, y)
      else
        call pgdraw(x, y)
      end if
    end do
  end subroutine draw_circle

  subroutine render_static(x1, y1, x2, y2, vx1, vy1, vx2, vy2, &
                           tx1, ty1, tx2, ty2, vx1n, vy1n, vx2n, vy2n, &
                           r, m1, m2, xmn, xmx, ymn, ymx)
    real, intent(in) :: x1, y1, x2, y2, vx1, vy1, vx2, vy2, &
                        tx1, ty1, tx2, ty2, vx1n, vy1n, vx2n, vy2n, &
                        r, m1, m2, xmn, xmx, ymn, ymx
    character(len=64) :: str
    call pgpanl(1, 1)
    call pgeras()

    call pgvstd()
    call pgvport(0.15, 0.85, 0.20, 0.82)

    call pgsci(1)
    call pgslw(1)
    call pgwnad(xmn, xmx, ymn, ymx)
    call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    call pglab('X', 'Y', 'Collision Result')
    
    call pgslw(2); call pgsci(1)
    call pgmove(x1, y1); call pgdraw(tx1, ty1)
    call pgmove(x2, y2); call pgdraw(tx2, ty2)
    
    call pgsci(2); call draw_circle(tx1, ty1, r)
    call pgsci(4); call draw_circle(tx2, ty2, r)
    
    call pgslw(5)
    call pgsci(2); call pgarro(tx1, ty1, tx1 + vx1n, ty1 + vy1n)
    call pgsci(4); call pgarro(tx2, ty2, tx2 + vx2n, ty2 + vy2n)

    call pgsci(1)
    call pgsch(1.4) 
    
    write(str, '(A, F0.1, A, F0.2, A, F0.2, A)') "m1:", m1, " V1:(", vx1, ",", vy1, ")"
    call pgmtxt('T', 1.2, 0.0, 0.0, str)
    write(str, '(A, F0.1, A, F0.2, A, F0.2, A)') "m2:", m2, " V2:(", vx2, ",", vy2, ")"
    call pgmtxt('T', 1.2, 1.0, 1.0, str)

    write(str, '(A, F0.2, A, F0.2, A)') "V1': (", vx1n, ",", vy1n, ")"
    call pgmtxt('B', 3.2, 0.0, 0.0, str)
    write(str, '(A, F0.2, A, F0.2, A)') "V2': (", vx2n, ",", vy2n, ")"
    call pgmtxt('B', 3.2, 1.0, 1.0, str)
    
    call pgsch(1.8)
  end subroutine render_static

  subroutine render_dynamic(x1, y1, x2, y2, tx1, ty1, tx2, ty2, &
                            cx1, cy1, cx2, cy2, r, xmn, xmx, ymn, ymx, step, t_curr, t_c)
    real, intent(in) :: x1, y1, x2, y2, tx1, ty1, tx2, ty2, cx1, cy1, cx2, cy2
    real, intent(in) :: r, xmn, xmx, ymn, ymx, t_curr, t_c
    integer, intent(in) :: step
    character(len=40) :: info
    call pgpanl(1, 2)
    call pgeras()
    call pgvstd()
    call pgvport(0.15, 0.85, 0.15, 0.85)
    call pgsci(1); call pgslw(1)
    call pgwnad(xmn, xmx, ymn, ymx)
    call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    write(info, '(A, I0, A)') 'Simulation: [A/D] Step ', step, ' (Q to quit)'
    call pglab('X', 'Y', info)

    call pgsls(2); call pgslw(2)
    call pgsci(2); call pgmove(x1, y1)
    if (t_curr <= t_c) then
        call pgdraw(cx1, cy1)
    else
        call pgdraw(tx1, ty1); call pgdraw(cx1, cy1)
    end if

    call pgsci(4); call pgmove(x2, y2)
    if (t_curr <= t_c) then
        call pgdraw(cx2, cy2)
    else
        call pgdraw(tx2, ty2); call pgdraw(cx2, cy2)
    end if

    call pgsls(1); call pgslw(4)
    call pgsci(2); call draw_circle(cx1, cy1, r)
    call pgsci(4); call draw_circle(cx2, cy2, r)
  end subroutine render_dynamic
end module lab_functions

program lab_7
  use lab_functions
  implicit none
  real :: r, m1, m2, x1, y1, vx1, vy1, x2, y2, vx2, vy2
  real :: tx1, ty1, tx2, ty2, vx1_new, vy1_new, vx2_new, vy2_new
  real :: dx0, dy0, dvx0, dvy0, a, b, c, delta, t_c, t_max, curr_t
  real :: dx, dy, dist_sq, dvx, dvy, dot_val, mf1, mf2
  real :: xmin, xmax, ymin, ymax, margin, dummy_x, dummy_y
  real :: curx1, cury1, curx2, cury2
  logical :: collided, looping
  integer :: ier, pgopen, status, n_step, max_steps
  character(len=100) :: filename
  character :: ch

  write(*,'(A)',advance='no') "Input file: "
  read(*,*) filename
  open(unit=10, file=trim(filename), status='old', iostat=status)
  if (status /= 0) stop "File error"
  read(10, *) r
  read(10, *) m1, m2
  read(10, *) x1, y1, vx1, vy1
  read(10, *) x2, y2, vx2, vy2
  close(10)

  write(*,*) "--- Input Data ---"
  write(*,'(A, F5.2)') " Radius: ", r
  write(*,'(A, 2F6.2)') " Masses: ", m1, m2
  write(*,'(A, 4F7.2)') " Ball 1: ", x1, y1, vx1, vy1
  write(*,'(A, 4F7.2)') " Ball 2: ", x2, y2, vx2, vy2

  dx0 = x2 - x1; dy0 = y2 - y1; dvx0 = vx2 - vx1; dvy0 = vy2 - vy1
  a = dvx0**2 + dvy0**2
  b = 2.0 * (dx0 * dvx0 + dy0 * dvy0)
  c = dx0**2 + dy0**2 - 4.0 * r**2
  
  collided = .false.
  if (c <= 0.0) then
    t_c = 0.0; collided = .true.
  else if (a > 0.0 .and. b < 0.0) then
    delta = b**2 - 4.0 * a * c
    if (delta >= 0.0) then
      t_c = (-b - sqrt(delta)) / (2.0 * a)
      if (t_c >= 0.0) collided = .true.
    end if
  end if
  if (.not. collided) stop "No collision predicted"

  tx1 = x1 + vx1 * t_c; ty1 = y1 + vy1 * t_c
  tx2 = x2 + vx2 * t_c; ty2 = y2 + vy2 * t_c
  dx = tx1 - tx2; dy = ty1 - ty2
  dist_sq = dx**2 + dy**2
  dvx = vx1 - vx2; dvy = vy1 - vy2
  dot_val = dvx * dx + dvy * dy
  mf1 = 2.0 * m2 / (m1 + m2); mf2 = 2.0 * m1 / (m1 + m2)
  vx1_new = vx1 - mf1 * (dot_val / dist_sq) * dx
  vy1_new = vy1 - mf1 * (dot_val / dist_sq) * dy
  vx2_new = vx2 - mf2 * (dot_val / dist_sq) * (-dx)
  vy2_new = vy2 - mf2 * (dot_val / dist_sq) * (-dy)

  write(*,*) "--- Results ---"
  write(*,'(A, F8.3)') " Time of Collision: ", t_c
  write(*,'(A, 2F8.3)') " Final V1: ", vx1_new, vy1_new
  write(*,'(A, 2F8.3)') " Final V2: ", vx2_new, vy2_new

  t_max = t_c * 2.0
  if (t_c == 0.0) t_max = 2.0
  margin = 4.0 * r
  xmin = min(x1, x2, tx1 + vx1_new*(t_max-t_c), tx2 + vx2_new*(t_max-t_c)) - margin
  xmax = max(x1, x2, tx1 + vx1_new*(t_max-t_c), tx2 + vx2_new*(t_max-t_c)) + margin
  ymin = min(y1, y2, ty1 + vy1_new*(t_max-t_c), ty2 + vy2_new*(t_max-t_c)) - margin
  ymax = max(y1, y2, ty1 + vy1_new*(t_max-t_c), ty2 + vy2_new*(t_max-t_c)) + margin

  ier = pgopen('/XSERVE')
  if (ier <= 0) stop

  call pgpap(10.0, 0.9)       
  call pgsch(1.8)             
  call pgscr(0, 1.0, 1.0, 1.0) 
  call pgscr(1, 0.0, 0.0, 0.0) 
  
  call pgask(.false.)
  call pgsubp(1, 2)

  n_step = 0; max_steps = 50; looping = .true.

  do while (looping)
    curr_t = (real(n_step) / real(max_steps)) * t_max
    if (curr_t <= t_c) then
      curx1 = x1 + vx1 * curr_t; cury1 = y1 + vy1 * curr_t
      curx2 = x2 + vx2 * curr_t; cury2 = y2 + vy2 * curr_t
    else
      curx1 = tx1 + vx1_new * (curr_t - t_c); cury1 = ty1 + vy1_new * (curr_t - t_c)
      curx2 = tx2 + vx2_new * (curr_t - t_c); cury2 = ty2 + vy2_new * (curr_t - t_c)
    end if

    call pgbbuf()
    call render_static(x1, y1, x2, y2, vx1, vy1, vx2, vy2, &
                       tx1, ty1, tx2, ty2, vx1_new, vy1_new, vx2_new, vy2_new, &
                       r, m1, m2, xmin, xmax, ymin, ymax)
    call render_dynamic(x1, y1, x2, y2, tx1, ty1, tx2, ty2, &
                        curx1, cury1, curx2, cury2, r, xmin, xmax, ymin, ymax, n_step, curr_t, t_c)
    call pgebuf()

    call pgcurs(dummy_x, dummy_y, ch)
    if (ch == 'a' .or. ch == 'A') then
      if (n_step > 0) n_step = n_step - 1
    else if (ch == 'd' .or. ch == 'D') then
      if (n_step < max_steps) n_step = n_step + 1
    else if (ch == 'q' .or. ch == 'Q') then
      looping = .false.
    end if
  end do

  call pgend()
end program lab_7