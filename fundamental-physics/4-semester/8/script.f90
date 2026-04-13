module lab_functions
  implicit none

  real, parameter :: eps = 1e-3

  contains

  subroutine init_bounds(T, nx, ny, hx, hy, dd, mm)
    integer, intent(in) :: nx, ny
    real, intent(in) :: hx, hy, dd, mm
    real, intent(inout) :: T(0:ny, 0:nx)
    integer :: i, j

    T = 0.0
    do i = 1, nx - 1
      T(0, i) = i * hx * dd
    end do
    do i = 1, nx - 1
      T(ny, i) = i * hx * mm
    end do
    do j = 1, ny - 1
      T(j, nx) = dd + j * hy * mm
    end do
  end subroutine init_bounds

  subroutine compute_step(T, nx, ny, hx, hy, converged)
    integer, intent(in) :: nx, ny
    real, intent(in) :: hx, hy
    real, intent(inout) :: T(0:ny, 0:nx)
    logical, intent(out) :: converged
    integer :: i, j
    real :: old_val, new_val, max_diff, coeff

    max_diff = 0.0
    converged = .false.
    coeff = 1.0 / (hx**2) + 1.0 / (hy**2)

    do j = 1, ny - 1
      do i = 1, nx - 1
        old_val = T(j, i)
        new_val = (1.0 / coeff) * ((T(j, i+1) + T(j, i-1)) / hx**2 + &
                  (T(j+1, i) + T(j-1, i)) / hy**2) / 2.0
        if (abs(new_val - old_val) > max_diff) then
          max_diff = abs(new_val - old_val)
        end if
        T(j, i) = new_val
      end do
    end do
    if (max_diff < eps) then
      converged = .true.
    end if
  end subroutine compute_step

  subroutine draw_circle(x, y, color_idx)
    real, intent(in) :: x, y
    integer, intent(in) :: color_idx

    call pgsci(0)
    call pgsfs(1)
    call pgcirc(x, y, 0.05)
    
    call pgsci(color_idx)
    call pgslw(10)
    call pgsfs(2)
    call pgcirc(x, y, 0.05)
    call pgslw(1)
  end subroutine draw_circle

  subroutine draw_node(x, y, temp, T_min, T_max, marked)
    real, intent(in) :: x, y, temp, T_min, T_max
    logical, intent(in) :: marked
    character(len=8) :: val_str
    integer :: color_idx

    color_idx = 16 + int(63.0 * (temp - T_min) / max(T_max - T_min, 1e-8))
    if (color_idx < 16) color_idx = 16
    if (color_idx > 79) color_idx = 79

    call draw_circle(x, y, color_idx)

    if (marked) then
      call pgslw(6)
      call pgcirc(x, y, 0.04)
      call pgslw(1) 
    end if
    
    call pgsci(1)
    call pgsch(0.5)
    write(val_str, '(F0.2)') temp
    call pgptxt(x, y-0.005, 0.0, 0.5, trim(val_str))
  end subroutine draw_node

  subroutine draw_grid(T, T_prev, nx, ny, hx, hy, dd, mm, step_idx, step_total)
    integer, intent(in) :: nx, ny, dd, mm, step_idx, step_total
    real, intent(in) :: hx, hy, T(0:ny, 0:nx), T_prev(0:ny, 0:nx)
    character(len=80) :: lbl_b, lbl_t, lbl_r, lbl_l
    integer :: i, j
    real :: x, y, T_min, T_max
    logical :: is_corner, has_changed
    character(len=64) :: title

    T_min = 0.0
    T_max = max(1.0, maxval(T))

    call pgpage()
    call pgvstd()
    call pgwnad(-0.1, 1.1, -0.1, 1.1)
    
    call pgsci(1)
    call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    write(title, '("Step: ", I0, "/", I0, " | A: Prev, D: Next, Q: Quit")') step_idx, step_total
    call pglab('X', 'Y', title)

    call pgsci(15)
    do i = 0, nx
      call pgmove(real(i)*hx, 0.0)
      call pgdraw(real(i)*hx, 1.0)
    end do
    do j = 0, ny
      call pgmove(0.0, real(j)*hy)
      call pgdraw(1.0, real(j)*hy)
    end do

    do j = 0, ny
      do i = 0, nx
        is_corner = ((i == 0 .or. i == nx) .and. (j == 0 .or. j == ny))
        if (.not. is_corner) then
          x = real(i) * hx
          y = real(j) * hy
          has_changed = (abs(T(j, i) - T_prev(j, i)) > eps)
          call draw_node(x, y, T(j, i), T_min, T_max, has_changed)
        end if
      end do
    end do

    write(lbl_b, '("T = i * hx * DD = i * ", F5.3, " * ", I0)') hx, dd
    write(lbl_t, '("T = i * hx * MM = i * ", F5.3, " * ", I0)') hx, mm
    write(lbl_l, '("T = 0")')
    write(lbl_r, '("T = DD + j * hy * MM = ", I0, " + j * ", F5.3, " * ", I0)') dd, hy, mm

    call pgsci(14)
    call pgsch(0.7)

    call pgmtxt('B', 5.5, 0.5, 0.5, trim(lbl_b))
    call pgmtxt('T', 1.2, 0.5, 0.5, trim(lbl_t))
    call pgmtxt('L', 4.5, 0.5, 0.5, trim(lbl_l))
    call pgmtxt('R', 2.0, 0.5, 0.5, trim(lbl_r))
    
    call pgsch(1.0)
    call pgsci(1)
  end subroutine draw_grid

  subroutine save_final_results(T, nx, ny)
    integer, intent(in) :: nx, ny
    real, intent(in) :: T(0:ny, 0:nx)
    integer :: i, j

    print *, ""
    print *, "--- Final temperature table ---"
    do j = ny, 0, -1
      print '(10F8.2)', (T(j, i), i = 0, nx)
    end do
  end subroutine save_final_results
end module lab_functions

program lab_8
  use lab_functions
  implicit none

  integer, parameter :: NX = 9, NY = 7, MAX_STEPS = 5000
  real, parameter :: hx = 1.0/9.0, hy = 1.0/7.0
  real :: history(0:NY, 0:NX, 0:MAX_STEPS)
  real :: DD, MM, px, py
  integer :: status, pgopen, total_steps, current_step
  character(len=64) :: filename
  character(len=1) :: key
  logical :: is_done, do_render
  real :: r(2), g(2), b(2), l(2)

  write(*, '(A)', advance='no') "Input file: "
  read(*, *) filename

  open(unit=10, file=trim(filename), status='old', iostat=status)
  if (status /= 0) stop "Error: Cannot open file"
  read(10, *, iostat=status) DD, MM
  if (status /= 0) stop "Error: Reading DD, MM (check file format)"
  close(10)

  call init_bounds(history(:,:,0), NX, NY, hx, hy, DD, MM)

  is_done = .false.
  total_steps = 0
  do while (.not. is_done .and. total_steps < MAX_STEPS)
    history(:,:,total_steps + 1) = history(:,:,total_steps)
    call compute_step(history(:,:,total_steps + 1), NX, NY, hx, hy, is_done)
    total_steps = total_steps + 1
  end do

  write(*, *) "Algorithm converged in ", total_steps, " steps."

  call save_final_results(history(:,:,total_steps), NX, NY)

  if (pgopen('/XSERVE') <= 0) stop

  l = (/0.0, 1.0/)
  r = (/0.0, 1.0/)
  g = (/0.0, 0.0/)
  b = (/1.0, 0.0/)

  call pgask(.false.)
  call pgscr(0, 1.0, 1.0, 1.0) 
  call pgscr(1, 0.0, 0.0, 0.0) 
  call pgscir(16, 79)
  call pgctab(l, r, g, b, 2, 1.0, 0.5)

  current_step = 0
  do_render = .true.
  key = ' '
  do while (key /= 'q' .and. key /= 'Q')
    if (do_render) then
      if (current_step > 0) then
        call draw_grid(history(:,:,current_step), history(:,:,current_step-1), &
                       NX, NY, hx, hy, int(DD), int(MM), current_step, total_steps)
      else
        call draw_grid(history(:,:,0), history(:,:,0), NX, NY, hx, hy, &
                       int(DD), int(MM), 0, total_steps)
      end if
      do_render = .false.
    end if

    call pgcurs(px, py, key)
    
    if ((key == 'd' .or. key == 'D') .and. current_step < total_steps) then
      current_step = current_step + 1
      do_render = .true.
    else if ((key == 'a' .or. key == 'A') .and. current_step > 0) then
      current_step = current_step - 1
      do_render = .true.
    else if (key == 'w' .or. key == 'W') then
      if (current_step /= total_steps) then
        current_step = total_steps
        do_render = .true.
      end if
    else if (key == 's' .or. key == 'S') then
      if (current_step /= 0) then
        current_step = 0
        do_render = .true.
      end if
    end if
  end do

  call pgend()
  write(*, *) "Session ended."
end program lab_8