module lab_functions
  implicit none

  contains

  subroutine init_conditions(u, v, Nx, L, x0, h, dx, mode, width, v0)
    integer, intent(in) :: Nx, mode
    real, intent(in) :: L, x0, h, dx, width, v0
    real, intent(out) :: u(0:Nx), v(0:Nx)
    integer :: i
    real :: x, dist, pi

    pi = acos(-1.0)
    u = 0.0
    v = 0.0

    do i = 0, Nx
      x = i * dx
      dist = abs(x - x0)

      select case (mode)
      case (1) ! Локальный линейный щипок
        if (dist <= width) then
          u(i) = h * (1.0 - dist / width)
        end if
      case (2) ! Глобальный линейный щипок
        if (x <= x0) then
          u(i) = h * x / x0
        else
          u(i) = h * (L - x) / (L - x0)
        end if
      case (3) ! Локальный синусоидальный щипок
        if (dist <= width) then
          u(i) = h * cos((pi * dist) / (2.0 * width))
        end if
      case (4) ! Локальный импульс скорости
        if (dist <= width) then
          v(i) = v0
        end if
      case (5) ! Глобальный импульс скорости
        v(i) = v0
      case (6) ! Локальный прямоугольный щипок
        if (dist <= width) then
          u(i) = h
        end if
      end select
    end do
    ! Закрепленные концы
    u(0) = 0.0
    u(Nx) = 0.0
    v(0) = 0.0
    v(Nx) = 0.0
  end subroutine init_conditions

  subroutine compute_first_step(u_next, u_curr, v_curr, Nx, C_sq, dt)
    integer, intent(in) :: Nx
    real, intent(in) :: C_sq, dt
    real, intent(in) :: u_curr(0:Nx), v_curr(0:Nx)
    real, intent(out) :: u_next(0:Nx)
    integer :: i

    do i = 1, Nx - 1
      u_next(i) = u_curr(i) + v_curr(i) * dt + 0.5 * C_sq * &
                  (u_curr(i+1) - 2.0 * u_curr(i) + u_curr(i-1))
    end do
    u_next(0) = 0.0
    u_next(Nx) = 0.0
  end subroutine compute_first_step

  subroutine compute_step(u_next, u_curr, u_prev, Nx, C_sq)
    integer, intent(in) :: Nx
    real, intent(in) :: C_sq
    real, intent(in) :: u_curr(0:Nx), u_prev(0:Nx)
    real, intent(out) :: u_next(0:Nx)
    integer :: i

    do i = 1, Nx - 1
      u_next(i) = 2.0 * u_curr(i) - u_prev(i) + C_sq * &
                  (u_curr(i+1) - 2.0 * u_curr(i) + u_curr(i-1))
    end do
    u_next(0) = 0.0
    u_next(Nx) = 0.0
  end subroutine compute_step

  subroutine draw_string(u, Nx, L, h, t_curr)
    integer, intent(in) :: Nx
    real, intent(in) :: L, h, t_curr
    real, intent(in) :: u(0:Nx)
    integer :: i
    real, allocatable :: x_vals(:)
    character(len=64) :: title

    allocate(x_vals(0:Nx))
    do i = 0, Nx
      x_vals(i) = i * (L / Nx)
    end do

    call pgpage()
    call pgvstd()
    call pgwnad(-0.1 * L, 1.1 * L, -1.5 * h, 1.5 * h)
    
    call pgsci(1)
    call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    write(title, '("Time: ", F8.4, " s | A: Prev, D: Next, S: T=0, Q: Quit")') t_curr
    call pglab('X (m)', 'U (m)', title)

    call pgsci(2)
    call pgslw(4)
    call pgline(Nx + 1, x_vals, u)
    call pgslw(1)
    
    call pgsci(1)
    deallocate(x_vals)
  end subroutine draw_string
end module lab_functions

program lab_10
  use lab_functions
  implicit none

  real :: L, x0, h_amp, T0, lambda, t_max, width, v0
  integer :: Nx, Nt, j, status, pgopen, current_step, mode, i_frame
  real :: dx, dt, c_wave, C_sq, px, py
  real, allocatable :: history(:,:), init_v(:)
  character(len=64) :: filename
  character(len=100) :: frame_name
  character(len=1) :: key
  logical :: do_render
  real :: period
  integer :: frames_per_period, step_stride, max_gif_step, do_gif

  write(*, '(A)', advance='no') "Input file: "
  read(*, *) filename

  open(unit=10, file=trim(filename), status='old', iostat=status)
  if (status /= 0) stop "Error: Cannot open file"
  read(10, *) L        ! Длина нити
  read(10, *) x0       ! Координата воздействия
  read(10, *) h_amp    ! Амплитуда (высота или характерное смещение)
  read(10, *) T0       ! Натяжение
  read(10, *) lambda   ! Линейная плотность
  read(10, *) t_max    ! Максимальное время
  read(10, *) Nx       ! Число узлов
  read(10, *) mode     ! Режим (1-5)
  read(10, *) width    ! Ширина области dx (для режимов 1, 3, 4)
  read(10, *) v0       ! Начальная скорость (для режимов 4, 5)
  read(10, *) do_gif   ! Генерировать GIF?
  close(10)

  c_wave = sqrt(T0 / lambda)
  dx = L / Nx
  dt = dx / c_wave 
  C_sq = (c_wave * dt / dx)**2
  Nt = int(t_max / dt)

  allocate(history(0:Nx, 0:Nt))
  allocate(init_v(0:Nx))

  call init_conditions(history(:,0), init_v, Nx, L, x0, h_amp, dx, mode, width, v0)

  if (Nt >= 1) then
    call compute_first_step(history(:,1), history(:,0), init_v, Nx, C_sq, dt)
  end if

  do j = 1, Nt - 1
    call compute_step(history(:,j+1), history(:,j), history(:,j-1), Nx, C_sq)
  end do

  period = 2.0 * L / c_wave
  frames_per_period = 50 
  step_stride = max(1, int((period / dt) / frames_per_period))
  max_gif_step = min(Nt, int(period / dt))

  write(*, '("Period: ", F8.4, " s")') period
  
  if (do_gif == 1) then
    call EXECUTE_COMMAND_LINE("mkdir -p frames")
    
    j = 0
    do i_frame = 0, max_gif_step, step_stride
      write(frame_name, '(A, I4.4, A)') 'frames/frame_', j, '.ps/CPS'
      if (pgopen(trim(frame_name)) > 0) then
        call pgscr(0, 1.0, 1.0, 1.0)
        call pgscr(1, 0.0, 0.0, 0.0)
        call pgscr(2, 0.0, 0.4, 0.8)
        call draw_string(history(:,i_frame), Nx, L, h_amp, i_frame * dt)
        call pgend()
      end if
      j = j + 1
    end do

    call EXECUTE_COMMAND_LINE("python3 make_gif.py")
  end if

  write(*, *) "Starting interactive mode..."

  if (pgopen('/XSERVE') <= 0) stop

  call pgask(.false.)
  call pgscr(0, 1.0, 1.0, 1.0) ! Белый фон
  call pgscr(1, 0.0, 0.0, 0.0) ! Черные оси
  call pgscr(2, 0.0, 0.4, 0.8) ! Синяя нить

  current_step = 0
  do_render = .true.
  key = ' '

  do while (key /= 'q' .and. key /= 'Q')
    if (do_render) then
      call draw_string(history(:,current_step), Nx, L, h_amp, current_step * dt)
      do_render = .false.
    end if

    call pgcurs(px, py, key)
    
    if ((key == 'd' .or. key == 'D') .and. current_step < Nt) then
      current_step = current_step + 1
      do_render = .true.
    else if ((key == 'a' .or. key == 'A') .and. current_step > 0) then
      current_step = current_step - 1
      do_render = .true.
    else if (key == 's' .or. key == 'S') then
      if (current_step /= 0) then
        current_step = 0
        do_render = .true.
      end if
    end if
  end do

  call pgend()
  deallocate(history, init_v)
  write(*, *) "Simulation finished."
end program lab_10