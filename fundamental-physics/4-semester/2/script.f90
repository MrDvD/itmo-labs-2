module lab_functions
  implicit none

  real, parameter :: pi = 3.1415926
  real, parameter :: eps = 0.5
  real, parameter :: g = 9.81

  type :: bonus_type
    real :: t
    logical :: reached
  end type bonus_type

contains
  real function get_real(msg)
    implicit none

    character(len=*), intent(in) :: msg

    write(0,'(AX)',advance='no') trim(msg)
    read*, get_real
  end function get_real

  function f_euler(vector, tau)
    implicit none

    real, dimension(4), intent(in) :: vector
    real, intent(in) :: tau
    real, dimension(4) :: f_euler

    f_euler(1) = vector(1) + tau * vector(3)
    f_euler(2) = vector(2) + tau * vector(4)
    f_euler(3) = vector(3)
    f_euler(4) = vector(4) - g * tau
  end function f_euler

  function f_runge_kutta(vector, tau)
    implicit none

    real, dimension(4), intent(in) :: vector
    real, intent(in) :: tau
    real, dimension(4) :: f_runge_kutta

    f_runge_kutta(1) = vector(1) + tau * vector(3)
    f_runge_kutta(2) = vector(2) + tau * vector(4) - g / 2 * tau ** 2
    f_runge_kutta(3) = vector(3)
    f_runge_kutta(4) = vector(4) - g * tau
  end function f_runge_kutta

  logical function print_table_row(vector, with_header, t)
    real, dimension(4), intent(in) :: vector
    logical, intent(in) :: with_header
    real, intent(in) :: t
    
    character(len=1) :: energy_status
    real :: K, U, energy_diff
    
    ! Calculate energies (assuming mass = 1)
    U = g * vector(2)
    K = 0.5 * (vector(3) ** 2 + vector(4) ** 2)
    energy_diff = abs(K - U)
    
    if (with_header) then
      write(*, '(A6, T8, A8, T16, A8, T24, A8, T32, A8, T40, A8, T48, A8, T56, A8, T65, A)') &
        't', 'x', 'y', 'v_x', 'v_y', 'U', 'K', '|U-K|', 'U=K?'
    end if

    ! Check if kinetic and potential energy are equal
    print_table_row = energy_diff < eps

    if (print_table_row) then
      energy_status = '+'
    else
      energy_status = '-'
    end if
    
    write(*, '(F6.2, T8, F8.2, T16, F8.2, T24, F8.2, T32, F8.2, T40, F8.2, T48, F8.2, T56, F8.2, T65, A1)') &
      t, vector(1), vector(2), vector(3), vector(4), U, K, energy_diff, energy_status
  end function print_table_row

  subroutine write_csv_row(vector, with_header, t, file_unit)
    real, dimension(4), intent(in) :: vector
    logical, intent(in) :: with_header
    real, intent(in) :: t
    integer, intent(in) :: file_unit
    
    character(len=1) :: energy_status
    real :: K, U, energy_diff
    
    ! Calculate energies (assuming mass = 1)
    U = g * vector(2)
    K = 0.5 * (vector(3) ** 2 + vector(4) ** 2)
    energy_diff = abs(K - U)
    
    if (with_header) then
      write(file_unit, '(A)') 't,x,y,v_x,v_y,U,K,|U-K|,U=K?'
    end if

    ! Check if kinetic and potential energy are equal
    if (energy_diff < eps) then
      energy_status = '+'
    else
      energy_status = '-'
    end if
    
    write(file_unit, *) &
      t, ',', vector(1), ',', vector(2), ',', vector(3), ',', vector(4), ',', U, ',', K, ',', energy_diff, ',', energy_status
  end subroutine write_csv_row

  subroutine start_simulation(vector, tau, f_func, file_unit)
    implicit none

    real, dimension(4), intent(in) :: vector
    integer, intent(in) :: file_unit
    real, intent(in) :: tau
    real, dimension(4) :: prev_vector, new_vector
    type(bonus_type) :: bonus
    real :: t

    interface
      function f_func(v, t)
        implicit none
        real, dimension(4), intent(in) :: v
        real, intent(in) :: t
        real, dimension(4) :: f_func
      end function f_func
    end interface

    t = 0
    prev_vector = vector
    call write_csv_row(prev_vector, .true., t, file_unit)
    if (print_table_row(prev_vector, .true., t)) then
      bonus%reached = .true.
      bonus%t = t
    end if

    do
      t = t + tau
      new_vector = f_func(prev_vector, tau)
      if (new_vector(2) - prev_vector(2) <= 0 .and. new_vector(2) <= 0) then
        exit
      end if
      call write_csv_row(new_vector, .false., t, file_unit)
      if (print_table_row(new_vector, .false., t)) then
        bonus%reached = .true.
        bonus%t = t
      end if
      prev_vector = new_vector
    end do
    if (bonus%reached) then
      write(0, '(A, F0.2, A)') "Energy equality was reached at time t = ", bonus%t, " seconds"
    else
      write(0, '(A)') "Energy equality was not reached, according to measurements"
    end if
  end subroutine start_simulation
end module lab_functions

program lab_2
  use lab_functions
  implicit none

  real, dimension(4) :: vector
  real :: v_0, alpha, tau
  integer :: euler_unit = 10, rk_unit = 11

  vector(1) = get_real('Set x_0:')
  do
    vector(2) = get_real('Set y_0:')
    if (vector(2) < 0) then
      write(0,'(A)') "[err] Unsupported coordinate, it should be non-negative."
    else
      exit
    end if
  end do
  do
    v_0 = get_real('Set v_0:')
    if (v_0 < 0) then
      write(0,'(A)') "[err] Unsupported velocity, it should be non-negative."
    else
      exit
    end if
  end do
  do
    alpha = get_real('Set angle \alpha (in rad):')
    if (alpha > pi .or. alpha <= 0) then
      write(0,'(A)') "[err] Unsupported angle, \alpha should be in (0, pi)."
    else
      exit
    end if
  end do
  vector(3) = v_0 * cos(alpha)
  vector(4) = v_0 * sin(alpha)
  do
    tau = get_real('Set tau (time step):')
    if (tau <= 0) then
      write(0,'(A)') "[err] Unsupported time, it should positive."
    else
      exit
    end if
  end do

  open(unit=euler_unit, file='output_euler.csv', status='replace')
  open(unit=rk_unit, file='output_rk.csv', status='replace')

  write(*,*) "### Euler method:"
  call start_simulation(vector, tau, f_euler, euler_unit)
  
  write(*,*) "### Runge-Kutta method:"
  call start_simulation(vector, tau, f_runge_kutta, rk_unit)

  close(euler_unit)
  close(rk_unit)
end program lab_2