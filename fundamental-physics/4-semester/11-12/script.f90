module lab_params
  implicit none
  real, parameter :: PI = 3.1415926535
end module lab_params

module lab_functions
  use lab_params
  implicit none

  contains

  function get_u0(x, mode) result(val)
    real, intent(in) :: x
    integer, intent(in) :: mode
    real :: val
    val = 0.0
    select case (mode)
    case (1) ; val = f2_2(x)
    case (2) ; val = f3_2(x)
    case (3) ; val = f3_9(x)
    end select
  end function get_u0

  function get_v0(x, c, a, b) result(val)
    real, intent(in) :: x, c, a, b
    real :: val
    val = g(x, c, a, b)
  end function get_v0

  function integral_psi_ext(x1, x2, c, a, b, L) result(res)
    real, intent(in) :: x1, x2, c, a, b, L
    real :: res

    res = primitive_psi(x2, c, a, b, L) - primitive_psi(x1, c, a, b, L)
  end function integral_psi_ext

  recursive function primitive_psi(X, c, a, b, L) result(P)
    real, intent(in) :: X, c, a, b, L
    real :: P
    real :: two_L, x_mod
    real :: len_pos, len_neg
    
    two_L = 2.0 * L

    if (X < 0.0) then
      P = primitive_psi(-X, c, a, b, L)
      return
    end if

    if (two_L > 0.0) then
      x_mod = X - two_L * floor(X / two_L)
    else
      x_mod = X
    end if
    
    P = 0.0

    len_pos = max(0.0, min(x_mod, b) - max(0.0, a))
    if (x_mod > 0.0) then
       if (x_mod < a) then
         len_pos = 0.0
       else if (x_mod > b) then
         len_pos = b - a
       else
         len_pos = x_mod - a
       end if
       if (len_pos < 0.0) len_pos = 0.0
       P = P + c * len_pos
    end if
    
    if (x_mod > L) then
      if (x_mod < (2.0*L - b)) then
        len_neg = 0.0
      else if (x_mod > (2.0*L - a)) then
        len_neg = (2.0*L - a) - max(L, 2.0*L - b)
      else
        len_neg = x_mod - max(L, 2.0*L - b)
      end if
      
      if (len_neg < 0.0) len_neg = 0.0
      P = P - c * len_neg
    end if
    
  end function primitive_psi

  function f_ext(x, L, mode) result(res)
    real, intent(in) :: x, L
    integer, intent(in) :: mode
    real :: res, x_mod
    x_mod = x - 2.0 * L * floor(x / (2.0 * L))
    if (x_mod <= L) then
      res = get_u0(x_mod, mode)
    else
      res = -get_u0(2.0 * L - x_mod, mode)
    end if
  end function f_ext

  function integral_g(x1, x2, c, a, b) result(res)
    implicit none

    real, intent(in) :: x1, x2, c, a, b
    real :: res
    real :: lower, upper
    
    lower = min(x1, x2)
    upper = max(x1, x2)
    lower = max(lower, a)
    upper = min(upper, b)
    
    if (lower < upper) then
      res = c * (upper - lower)
    else
      res = 0.0
    end if
  end function integral_g

  subroutine calc_fourier_coeffs(An, Bn, Nx, L, mode, a_wave, a, b, n_max)
    integer, intent(in) :: Nx, mode, n_max
    real, intent(in) :: L, a, b, a_wave
    real, intent(out) :: An(n_max), Bn(n_max)
    integer :: n, i
    real :: x, dx, integral_u, integral_v, omega_n
    dx = L / real(Nx)
    do n = 1, n_max
      integral_u = 0.0 ; integral_v = 0.0
      omega_n = real(n) * PI * a_wave / L
      do i = 1, Nx - 1
        x = real(i) * dx
        integral_u = integral_u + get_u0(x, mode) * sin(real(n) * PI * x / L)
        integral_v = integral_v + get_v0(x, a_wave, a, b) * sin(real(n) * PI * x / L)
      end do
      An(n) = (2.0 / L) * integral_u * dx
      Bn(n) = (2.0 / (L * omega_n)) * integral_v * dx
    end do
  end subroutine calc_fourier_coeffs

  function f3_2(x)
    real, intent(in) :: x
    real :: f3_2
    f3_2 = x * x * sin(PI * x)
  end function f3_2

  function g(x, c, a, b)
    real, intent(in) :: x, c, a, b
    real :: g
    if (x < a .or. x > b) then ; g = 0.0 ; else ; g = c ; end if
  end function g

  function f2_2(x)
    real, intent(in) :: x
    real :: f2_2
    if (x < 0.0 .or. x > 2.0) then ; f2_2 = 0.0
    else if (x <= 0.5) then ; f2_2 = 3.0 * x
    else ; f2_2 = -x + 2.0 ; end if
  end function f2_2

  function f3_9(x)
    real, intent(in) :: x
    real :: f3_9
    f3_9 = exp(-x) * sin(PI * x)
  end function f3_9

  function calculate_mse(u_calc, u_ref, Nx) result(mse)
    implicit none

    integer, intent(in) :: Nx
    real, intent(in) :: u_calc(0:Nx), u_ref(0:Nx)
    real :: mse
    integer :: i
    mse = 0.0
    do i = 0, Nx
      mse = mse + (u_calc(i) - u_ref(i))**2
    end do
    mse = mse / real(Nx + 1)
  end function calculate_mse

  subroutine compute_step(u_next, u_curr, u_prev, Nx, C_sq)
    integer, intent(in) :: Nx
    real, intent(in) :: C_sq, u_curr(0:Nx), u_prev(0:Nx)
    real, intent(out) :: u_next(0:Nx)
    integer :: i
    do i = 1, Nx - 1
      u_next(i) = 2.0 * u_curr(i) - u_prev(i) + C_sq * (u_curr(i+1) - 2.0 * u_curr(i) + u_curr(i-1))
    end do
    u_next(0) = 0.0 ; u_next(Nx) = 0.0
  end subroutine compute_step

  subroutine draw_frame(u1, u2, u3, Nx, L, h, t_curr, mse_num, mse_fou, mode_flag)
    integer, intent(in) :: Nx, mode_flag
    real, intent(in) :: L, h, t_curr, u1(0:Nx), u2(0:Nx), u3(0:Nx), mse_num, mse_fou
    integer :: i
    real, allocatable :: x_vals(:)
    real :: lx(2), ly(2), x_pos, y_pos
    character(len=100) :: title, txt_num, txt_fou
    
    allocate(x_vals(0:Nx))
    do i = 0, Nx ; x_vals(i) = real(i) * (L / real(Nx)) ; end do

    call pgpage() ; call pgvstd()
    call pgwnad(-0.1 * L, 1.1 * L, -1.2 * h, 1.7 * h)
    call pgsci(1) ; call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    
    if (mode_flag == 4) then
      write(title, '("T: ", F6.3, "s | Comparison Mode")') t_curr
      call pglab('X (m)', 'U (m)', title)
      call pgsci(2) ; call pgline(Nx + 1, x_vals, u1) 
      call pgsci(3) ; call pgline(Nx + 1, x_vals, u2) 
      call pgsci(4) ; call pgline(Nx + 1, x_vals, u3) 

      x_pos = L * 0.55 ; y_pos = h * 1.55
      lx(1) = x_pos ; lx(2) = x_pos + L*0.05
      
      ! legend numerical
      ly(1) = y_pos ; ly(2) = y_pos
      write(txt_num, '("Numerical MSE: ", E9.2)') mse_num
      call pgsci(2) ; call pgline(2, lx, ly)
      call pgsci(1) ; call pgtext(x_pos + L*0.05, y_pos - h*0.02, trim(txt_num))
      
      ! legend analytical
      y_pos = y_pos - h * 0.12 ; ly(1) = y_pos ; ly(2) = y_pos
      call pgsci(3) ; call pgline(2, lx, ly)
      call pgsci(1) ; call pgtext(x_pos + L*0.05, y_pos - h*0.02, "Analytical (Ref)")
      
      ! legend fourier
      y_pos = y_pos - h * 0.12 ; ly(1) = y_pos ; ly(2) = y_pos
      write(txt_fou, '("Fourier MSE:   ", E9.2)') mse_fou
      call pgsci(4) ; call pgline(2, lx, ly)
      call pgsci(1) ; call pgtext(x_pos + L*0.05, y_pos - h*0.02, trim(txt_fou))
    else
      write(title, '("T: ", F6.3, "s | Single Method")') t_curr
      call pglab('X (m)', 'U (m)', title)
      call pgsci(2) ; call pgline(Nx + 1, x_vals, u1)
    end if
    deallocate(x_vals)
  end subroutine draw_frame
end module lab_functions

program lab_11_12
  use lab_functions
  use lab_params
  implicit none

  real :: L, T0, rho, t_max, dx, dt, a_wave, C_sq, t_curr, x_curr, px, py, c, a, b, h_max
  real :: mse_n, mse_f
  integer :: Nx, Nt, j, i, i_harm, status, pgopen, current_step, mode, calc_method, N_HARMONICS
  real, allocatable :: h_num(:,:), h_ana(:,:), h_fou(:,:), init_v(:), An(:), Bn(:)
  character(len=64) :: filename
  character(len=1) :: key

  write(*, '(A)', advance='no') "Input file: " ; read(*, *) filename
  write(*, '(A)') "Select: 1-Numerical, 2-Analytical, 3-Fourier, 4-All"
  read(*, *) calc_method

  open(unit=10, file=trim(filename), status='old', iostat=status)
  if (status /= 0) stop "Error: File not found"
  read(10, *) L, T0, rho, t_max, Nx, mode, a, b, c, N_HARMONICS
  close(10)

  a_wave = sqrt(T0 / rho) ; dx = L / real(Nx)
  dt = 0.9 * dx / a_wave 
  C_sq = (a_wave * dt / dx)**2 ; Nt = int(t_max / dt)

  allocate(h_num(0:Nx, 0:Nt), h_ana(0:Nx, 0:Nt), h_fou(0:Nx, 0:Nt))
  h_num = 0.0 ; h_ana = 0.0 ; h_fou = 0.0

  ! numerical
  if (calc_method == 1 .or. calc_method == 4) then
    allocate(init_v(0:Nx))
    do i = 0, Nx
      h_num(i,0) = get_u0(real(i)*dx, mode)
      init_v(i) = get_v0(real(i)*dx, c, a, b)
    end do
    do i = 1, Nx - 1
      h_num(i,1) = h_num(i,0) + init_v(i)*dt + 0.5*C_sq*(h_num(i+1,0)-2.0*h_num(i,0)+h_num(i-1,0))
    end do
    do j = 1, Nt - 1
      call compute_step(h_num(:,j+1), h_num(:,j), h_num(:,j-1), Nx, C_sq)
    end do
    deallocate(init_v)
  end if

  ! analytical
  if (calc_method == 2 .or. calc_method == 4) then
    do j = 0, Nt
      t_curr = real(j) * dt
      do i = 0, Nx
        x_curr = real(i) * dx
        
        h_ana(i,j) = 0.5 * (f_ext(x_curr - a_wave*t_curr, L, mode) + &
                            f_ext(x_curr + a_wave*t_curr, L, mode))
        h_ana(i,j) = h_ana(i,j) + &
                     (1.0 / (2.0 * a_wave)) * &
                     integral_psi_ext(x_curr - a_wave*t_curr, x_curr + a_wave*t_curr, c, a, b, L)
      end do
    end do
  end if

  ! fourier
  if (calc_method == 3 .or. calc_method == 4) then
    allocate(An(N_HARMONICS), Bn(N_HARMONICS))
    call calc_fourier_coeffs(An, Bn, Nx, L, mode, a_wave, a, b, N_HARMONICS)
    do j = 0, Nt
      t_curr = real(j) * dt
      do i = 0, Nx
        x_curr = real(i) * dx
        do i_harm = 1, N_HARMONICS
          h_fou(i,j) = h_fou(i,j) + (An(i_harm)*cos(real(i_harm)*PI*a_wave*t_curr/L) + &
                       Bn(i_harm)*sin(real(i_harm)*PI*a_wave*t_curr/L)) * sin(real(i_harm)*PI*x_curr/L)
        end do
      end do
    end do
    deallocate(An, Bn)
  end if

  if (pgopen('/XSERVE') <= 0) stop
  call pgask(.false.) ; call pgscr(0, 1.0, 1.0, 1.0) ; call pgscr(1, 0.0, 0.0, 0.0)
  
  h_max = 0.0
  do i = 0, Nx ; h_max = max(h_max, abs(h_ana(i,0)), abs(h_num(i,0))) ; end do
  if (h_max < 1e-5) h_max = 1.0

  current_step = 0 ; key = ' '
  do while (key /= 'q' .and. key /= 'Q')
    mse_n = calculate_mse(h_num(:,current_step), h_ana(:,current_step), Nx)
    mse_f = calculate_mse(h_fou(:,current_step), h_ana(:,current_step), Nx)

    if (calc_method == 4) then
      call draw_frame(h_num(:,current_step), h_ana(:,current_step), h_fou(:,current_step), &
                     Nx, L, h_max, real(current_step)*dt, mse_n, mse_f, 4)
    else if (calc_method == 1) then
      call draw_frame(h_num(:,current_step), h_num(:,current_step), h_num(:,current_step), &
                     Nx, L, h_max, real(current_step)*dt, 0.0, 0.0, 1)
    else if (calc_method == 2) then
      call draw_frame(h_ana(:,current_step), h_ana(:,current_step), h_ana(:,current_step), &
                     Nx, L, h_max, real(current_step)*dt, 0.0, 0.0, 1)
    else
      call draw_frame(h_fou(:,current_step), h_fou(:,current_step), h_fou(:,current_step), &
                     Nx, L, h_max, real(current_step)*dt, 0.0, 0.0, 1)
    end if
    
    call pgcurs(px, py, key)
    if ((key == 'd' .or. key == 'D') .and. current_step < Nt) current_step = current_step + 1
    if ((key == 'a' .or. key == 'A') .and. current_step > 0) current_step = current_step - 1
    if (key == 's' .or. key == 'S') current_step = 0
  end do

  call pgend()
  deallocate(h_num, h_ana, h_fou)
end program lab_11_12