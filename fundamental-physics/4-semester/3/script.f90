module lab_types
  type :: vector_system
    real, dimension(4) :: start, curr
  end type vector_system

  type :: time_system
    real :: t, tau
  end type time_system

  type :: function_system
    real, pointer :: x(:), y(:)
    integer :: count
  end type function_system
end module lab_types

module lab_functions
  use lab_types
  implicit none

  real, parameter :: pi = 3.1415926
  real, parameter :: eps = 0.5
  real, parameter :: g = 9.81

contains
  real function get_real(msg)
    character(len=*), intent(in) :: msg

    write(0,'(A,1X)',advance='no') trim(msg)
    read*, get_real
  end function get_real

  function f_practice(vector, time, k_m)
    type(vector_system), intent(in) :: vector
    type(time_system), intent(in) :: time
    real, intent(in) :: k_m
    real, dimension(4) :: f_practice

    f_practice(1) = vector%curr(1) + time%tau * vector%curr(3)
    f_practice(2) = vector%curr(2) + time%tau * vector%curr(4)
    f_practice(3) = vector%curr(3) - k_m * vector%curr(3) * time%tau
    f_practice(4) = vector%curr(4) - k_m * vector%curr(4) * time%tau - g * time%tau
  end function f_practice

  function f_theory(vector, time, k_m)
    type(vector_system), intent(in) :: vector
    type(time_system), intent(in) :: time
    real, intent(in) :: k_m
    real, dimension(4) :: f_theory

    f_theory(1) = vector%start(3) / k_m * (1 - exp(-k_m * time%t))
    f_theory(2) = (vector%start(4) / k_m + g / k_m ** 2) * (1 - exp(-k_m * time%t)) - g * time%t / k_m
    f_theory(3) = vector%start(3) * exp(-k_m * time%t)
    f_theory(4) = -g / k_m + (vector%start(4) + g / k_m) * exp(-k_m * time%t)
  end function f_theory

  subroutine print_table_row(vector, with_header, t)
    real, dimension(4), intent(in) :: vector
    logical, intent(in) :: with_header
    real, intent(in) :: t
    
    if (with_header) then
      write(*, '(A6, T8, A8, T16, A8, T24, A8, T32, A8)') &
        't', 'x', 'y', 'v_x', 'v_y'
    end if
    
    write(*, '(F6.2, T8, F8.2, T16, F8.2, T24, F8.2, T32, F8.2)') &
      t, vector(1), vector(2), vector(3), vector(4)
  end subroutine print_table_row

  subroutine write_csv_row(vector, with_header, t, file_unit)
    real, dimension(4), intent(in) :: vector
    logical, intent(in) :: with_header
    real, intent(in) :: t
    integer, intent(in) :: file_unit
    
    if (with_header) then
      write(file_unit, '(A)') 't,x,y,v_x,v_y'
    end if
    
    write(file_unit, *) &
      t, ',', vector(1), ',', vector(2), ',', vector(3), ',', vector(4)
  end subroutine write_csv_row

  subroutine resize(var, n)
    real, pointer :: var(:), tmp(:)
    integer, intent(in) :: n
    integer :: this_size

    if (associated(var)) then
      this_size = size(var, 1)
      allocate(tmp(this_size))
      tmp = var
      deallocate(var)
    end if

    allocate(var(n))

    if (associated(tmp)) then
      this_size = min(size(tmp, 1), size(var, 1))
      var(:this_size) = tmp(:this_size)
      deallocate(tmp)
    end if
  end subroutine resize

  subroutine draw_plot(x1, y1, x2, y2, n1, n2, file_name)
    real, dimension(:), intent(in) :: x1, y1, x2, y2
    integer, intent(in) :: n1, n2
    character(len=*), intent(in) :: file_name
    integer :: pgopen, ier
    ier = pgopen(file_name // '.ps/PS')
    if (ier .ne. 1) stop

    call pgenv(min(minval(x1), minval(x2)),&
               max(maxval(x1), maxval(x2)),&
               min(minval(y1), minval(y2)),&
               max(maxval(y1), maxval(y2)), 0, 1)
    call pglab('x', 'y', 'Theory (dashed) vs Practice (solid)')
    call pgsls(2)
    call pgline(n1, x1, y1)
    call pgpt(n1, x1, y1, 9)
    call pgsls(1)
    call pgline(n2, x2, y2)
    call pgpt(n2, x2, y2, 9)
    call pgend
  end subroutine draw_plot

  function start_simulation(vector, tau, k_m, f_func, file_unit)
    real, dimension(4), intent(in) :: vector
    type(function_system) :: start_simulation
    integer :: dots_cap = 4
    integer, intent(in) :: file_unit
    real, intent(in) :: tau, k_m
    type(vector_system) :: prev_vector
    real, dimension(4) :: new_vector
    type(time_system) :: time

    interface
      function f_func(v, t, k)
        use lab_types
        implicit none
        type(vector_system), intent(in) :: v
        type(time_system), intent(in) :: t
        real, intent(in) :: k
        real, dimension(4) :: f_func
      end function f_func
    end interface

    time%t = 0
    time%tau = tau
    prev_vector%start = vector
    prev_vector%curr = vector

    allocate(start_simulation%x(dots_cap))
    allocate(start_simulation%y(dots_cap))
    start_simulation%count = 1
    start_simulation%x(start_simulation%count) = vector(1)
    start_simulation%y(start_simulation%count) = vector(2)

    call write_csv_row(prev_vector%start, .true., time%t, file_unit)
    call print_table_row(prev_vector%start, .true., time%t)

    do
      time%t = time%t + time%tau
      new_vector = f_func(prev_vector, time, k_m)
      start_simulation%count = start_simulation%count + 1
      if (start_simulation%count == dots_cap) then
        dots_cap = start_simulation%count * 2
        call resize(start_simulation%x, dots_cap)
        call resize(start_simulation%y, dots_cap)
      end if
      start_simulation%x(start_simulation%count) = new_vector(1)
      start_simulation%y(start_simulation%count) = new_vector(2)
      call write_csv_row(new_vector, .false., time%t, file_unit)
      call print_table_row(new_vector, .false., time%t)
      if (new_vector(2) - prev_vector%curr(2) <= 0 .and. new_vector(2) <= 0) then
        exit
      end if
      prev_vector%curr = new_vector
    end do

    if (start_simulation%count < dots_cap) then
      call resize(start_simulation%x, start_simulation%count)
      call resize(start_simulation%y, start_simulation%count)
    end if
  end function start_simulation
end module lab_functions

program lab_3
  use lab_functions
  implicit none

  real, dimension(4) :: vector
  real :: v_0, alpha, tau, k_m
  integer :: practice_unit = 10, theory_unit = 11
  type(function_system) :: kinetics_theory, kinetics_practice

  vector(1) = 0
  vector(2) = 0
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
    k_m = get_real('Set k/m relation:')
    if (k_m <= 0) then
      write(0,'(A)') "[err] Unsupported relation, k/m should be positive."
    else
      exit
    end if
  end do
  do
    tau = get_real('Set tau (time step):')
    if (tau <= 0) then
      write(0,'(A)') "[err] Unsupported time, it should positive."
    else
      exit
    end if
  end do

  open(unit=practice_unit, file='output_practice.csv', status='replace')
  open(unit=theory_unit, file='output_theory.csv', status='replace')

  write(*,*) "### Theory:"
  kinetics_theory = start_simulation(vector, tau, k_m, f_theory, theory_unit)

  write(*,*) "### Practice:"
  kinetics_practice = start_simulation(vector, tau, k_m, f_practice, practice_unit)
  call draw_plot(kinetics_theory%x, kinetics_theory%y,&
                 kinetics_practice%x, kinetics_practice%y,&
                 kinetics_theory%count, kinetics_practice%count,&
                 "plot")

  close(practice_unit)
  close(theory_unit)
end program lab_3