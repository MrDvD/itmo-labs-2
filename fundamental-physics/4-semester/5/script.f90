module lab_types
  type :: body
    real :: m
    real, dimension(2) :: r, r_old, a
  end type body

  type :: coord_pointer
    real, pointer :: x(:) => null(), y(:) => null()
    real, pointer :: ax(:) => null(), ay(:) => null()
    real, pointer :: rox(:) => null(), roy(:) => null()
  end type coord_pointer

  type :: history
    type(coord_pointer) :: pos(2)
    real, pointer :: t_vals(:) => null()
    real :: min_x, min_y, max_x, max_y
    integer :: capacity, size, idx
  end type history

  type :: system_state
    type(body) :: b1, b2
    type(body) :: b1_init, b2_init
    real :: t, tau, tau_init
  end type system_state
end module lab_types

module lab_functions
  use lab_types
  implicit none

  real, parameter :: G = 1.0
  real, parameter :: PI = 3.1415926
  real, parameter :: eps = 1e-5
  
contains

  subroutine update_accelerations(state)
    type(system_state), intent(inout) :: state
    real, dimension(2) :: dist_vec
    real :: r, force

    dist_vec = state%b2%r - state%b1%r
    r = sqrt(sum(dist_vec**2))
    
    if (r < 0.01) r = 0.01

    force = G * state%b1%m * state%b2%m / (r**2)
    
    state%b1%a = (force / state%b1%m) * (dist_vec / r)
    state%b2%a = (force / state%b2%m) * (-dist_vec / r)
  end subroutine update_accelerations

  subroutine verlet_step(state)
    type(system_state), intent(inout) :: state
    real, dimension(2) :: next_r1, next_r2

    call update_accelerations(state)

    next_r1 = 2.0 * state%b1%r - state%b1%r_old + state%b1%a * state%tau**2
    next_r2 = 2.0 * state%b2%r - state%b2%r_old + state%b2%a * state%tau**2

    state%b1%r_old = state%b1%r
    state%b2%r_old = state%b2%r

    state%b1%r = next_r1
    state%b2%r = next_r2
  end subroutine verlet_step

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

  subroutine update_bounds_from_trace(hist, trace_length)
    type(history), intent(inout) :: hist
    integer, intent(in) :: trace_length
    integer :: i, start_idx

    start_idx = max(1, hist%idx - trace_length + 1)

    hist%min_x = min(hist%pos(1)%x(start_idx), hist%pos(2)%x(start_idx))
    hist%max_x = max(hist%pos(1)%x(start_idx), hist%pos(2)%x(start_idx))
    hist%min_y = min(hist%pos(1)%y(start_idx), hist%pos(2)%y(start_idx))
    hist%max_y = max(hist%pos(1)%y(start_idx), hist%pos(2)%y(start_idx))

    do i = start_idx + 1, hist%idx
      hist%min_x = min(hist%min_x, hist%pos(1)%x(i), hist%pos(2)%x(i))
      hist%max_x = max(hist%max_x, hist%pos(1)%x(i), hist%pos(2)%x(i))
      hist%min_y = min(hist%min_y, hist%pos(1)%y(i), hist%pos(2)%y(i))
      hist%max_y = max(hist%max_y, hist%pos(1)%y(i), hist%pos(2)%y(i))
    end do
  end subroutine update_bounds_from_trace

  subroutine load_state_from_history(hist, state)
    type(history), intent(in) :: hist
    type(system_state), intent(inout) :: state
    integer :: i
    i = hist%idx
    
    state%b1%r(1)     = hist%pos(1)%x(i)
    state%b1%r(2)     = hist%pos(1)%y(i)
    state%b1%a(1)     = hist%pos(1)%ax(i)
    state%b1%a(2)     = hist%pos(1)%ay(i)
    state%b1%r_old(1) = hist%pos(1)%rox(i)
    state%b1%r_old(2) = hist%pos(1)%roy(i)
    
    state%b2%r(1)     = hist%pos(2)%x(i)
    state%b2%r(2)     = hist%pos(2)%y(i)
    state%b2%a(1)     = hist%pos(2)%ax(i)
    state%b2%a(2)     = hist%pos(2)%ay(i)
    state%b2%r_old(1) = hist%pos(2)%rox(i)
    state%b2%r_old(2) = hist%pos(2)%roy(i)
    
    state%t = hist%t_vals(i)
  end subroutine load_state_from_history

  subroutine reset_simulation(sim, hist)
    type(system_state), intent(inout) :: sim
    type(history), intent(inout) :: hist

    sim%b1 = sim%b1_init
    sim%b2 = sim%b2_init
    sim%t = 0.0
    sim%tau = sim%tau_init

    hist%size = 0
    hist%idx = 1
    call append_history(hist, sim)
    
    hist%min_x = min(sim%b1%r(1), sim%b2%r(1))
    hist%max_x = max(sim%b1%r(1), sim%b2%r(1))
    hist%min_y = min(sim%b1%r(2), sim%b2%r(2))
    hist%max_y = max(sim%b1%r(2), sim%b2%r(2))
  end subroutine reset_simulation

  subroutine append_history(hist, state)
    type(history), intent(inout) :: hist
    type(system_state), intent(in) :: state
    integer :: i

    if (hist%size == hist%capacity) then
      hist%capacity = hist%capacity * 2
      do i = 1, 2
        call resize(hist%pos(i)%x, hist%capacity)
        call resize(hist%pos(i)%y, hist%capacity)
        call resize(hist%pos(i)%ax, hist%capacity)
        call resize(hist%pos(i)%ay, hist%capacity)
        call resize(hist%pos(i)%rox, hist%capacity)
        call resize(hist%pos(i)%roy, hist%capacity)
      end do
      call resize(hist%t_vals, hist%capacity)
    end if

    hist%size = hist%size + 1

    hist%pos(1)%x(hist%size) = state%b1%r(1)
    hist%pos(1)%y(hist%size) = state%b1%r(2)
    hist%pos(1)%ax(hist%size) = state%b1%a(1)
    hist%pos(1)%ay(hist%size) = state%b1%a(2)
    hist%pos(1)%rox(hist%size) = state%b1%r_old(1)
    hist%pos(1)%roy(hist%size) = state%b1%r_old(2)
    hist%pos(2)%x(hist%size) = state%b2%r(1)
    hist%pos(2)%y(hist%size) = state%b2%r(2)
    hist%pos(2)%ax(hist%size) = state%b2%a(1)
    hist%pos(2)%ay(hist%size) = state%b2%a(2)
    hist%pos(2)%rox(hist%size) = state%b2%r_old(1)
    hist%pos(2)%roy(hist%size) = state%b2%r_old(2)
    
    hist%t_vals(hist%size) = state%t
  end subroutine append_history

  subroutine simulate_interactive(sim1, sim2, trace_length)
    type(system_state), intent(inout) :: sim1, sim2
    integer, intent(in) :: trace_length
    integer :: pgopen, ier, left_bound_trace, n_points
    real :: unused
    character(len=1) :: ch
    character(len=20) :: t_str, tau_str
    type(history) :: curr_hist1, curr_hist2
    
    allocate(curr_hist1%pos(1)%x(16),&
             curr_hist1%pos(1)%y(16),&
             curr_hist1%pos(1)%ax(16),&
             curr_hist1%pos(1)%ay(16),&
             curr_hist1%pos(1)%rox(16),&
             curr_hist1%pos(1)%roy(16),&
             curr_hist1%pos(2)%x(16),&
             curr_hist1%pos(2)%y(16),&
             curr_hist1%pos(2)%ax(16),&
             curr_hist1%pos(2)%ay(16),&
             curr_hist1%pos(2)%rox(16),&
             curr_hist1%pos(2)%roy(16),&
             curr_hist1%t_vals(16))
    allocate(curr_hist2%pos(1)%x(16),&
             curr_hist2%pos(1)%y(16),&
             curr_hist2%pos(1)%ax(16),&
             curr_hist2%pos(1)%ay(16),&
             curr_hist2%pos(1)%rox(16),&
             curr_hist2%pos(1)%roy(16),&
             curr_hist2%pos(2)%x(16),&
             curr_hist2%pos(2)%y(16),&
             curr_hist2%pos(2)%ax(16),&
             curr_hist2%pos(2)%ay(16),&
             curr_hist2%pos(2)%rox(16),&
             curr_hist2%pos(2)%roy(16),&
             curr_hist2%t_vals(16))

    curr_hist1%capacity = 16
    curr_hist2%capacity = 16
    call reset_simulation(sim1, curr_hist1)
    call reset_simulation(sim2, curr_hist2)

    ier = pgopen('/XSERVE')
    if (ier .ne. 1) stop
    call pgask(.false.)
    call pgscr(0, 1.0, 1.0, 1.0) ! white background
    call pgscr(1, 0.0, 0.0, 0.0) ! black pen

    do
      call pgbbuf()
      call pgeras()
      call pgsci(1)
      call pgenv(min(curr_hist1%min_x, curr_hist2%min_x) - 1.0,&
                 max(curr_hist1%max_x, curr_hist2%max_x) + 1.0,&
                 min(curr_hist1%min_y, curr_hist2%min_y) - 1.0,&
                 max(curr_hist1%max_y, curr_hist2%max_y) + 1.0, 1, 0)
      write(t_str, '(A, F7.2, A)') 'T = ', sim1%t, 's'
      call pgmtxt('B', 2.0, 0.0, 0.5, t_str)
      write(tau_str, '(A, F7.3, A)') 'tau = ', sim1%tau, 's'
      call pgmtxt('B', 2.0, 1.0, 0.5, tau_str)
      call pglab('X', 'Y', 'D: Forward | A: Back | R: Reset | Q: Quit')

      ! draw trajectory
      if (curr_hist1%idx > 1 .and. trace_length > 0) then
        call pgsls(2); call pgsci(15)
        
        left_bound_trace = max(1, curr_hist1%idx - trace_length + 1)
        n_points = curr_hist1%idx - left_bound_trace + 1
        
        call pgline(n_points,&
                    curr_hist1%pos(1)%x(left_bound_trace:curr_hist1%idx),&
                    curr_hist1%pos(1)%y(left_bound_trace:curr_hist1%idx))
        call pgline(n_points,&
                    curr_hist1%pos(2)%x(left_bound_trace:curr_hist1%idx),&
                    curr_hist1%pos(2)%y(left_bound_trace:curr_hist1%idx))
        call pgline(n_points,&
                    curr_hist2%pos(1)%x(left_bound_trace:curr_hist2%idx),&
                    curr_hist2%pos(1)%y(left_bound_trace:curr_hist2%idx))
        call pgline(n_points,&
                    curr_hist2%pos(2)%x(left_bound_trace:curr_hist2%idx),&
                    curr_hist2%pos(2)%y(left_bound_trace:curr_hist2%idx))
      end if

      call pgsls(1)
      call pgsci(2); call pgpt(1, curr_hist1%pos(1)%x(curr_hist1%idx), curr_hist1%pos(1)%y(curr_hist1%idx), 17)
      call pgsci(4); call pgpt(1, curr_hist1%pos(2)%x(curr_hist1%idx), curr_hist1%pos(2)%y(curr_hist1%idx), 17)
      call pgsci(3); call pgpt(1, curr_hist2%pos(1)%x(curr_hist2%idx), curr_hist2%pos(1)%y(curr_hist2%idx), 17)
      call pgsci(5); call pgpt(1, curr_hist2%pos(2)%x(curr_hist2%idx), curr_hist2%pos(2)%y(curr_hist2%idx), 17)

      call pgband(0, 0, unused, unused, unused, unused, ch)

      select case (ch)
        case ('q', 'Q')
          exit
        
        case ('r', 'R')
          call reset_simulation(sim1, curr_hist1)
          call reset_simulation(sim2, curr_hist2)
          
        case ('d', 'D')
          if (curr_hist1%idx == curr_hist1%size) then
            call verlet_step(sim1)
            call verlet_step(sim2)
            sim1%t = sim1%t + sim1%tau
            sim2%t = sim2%t + sim2%tau
            call append_history(curr_hist1, sim1)
            call append_history(curr_hist2, sim2)
          end if
          curr_hist1%idx = curr_hist1%idx + 1
          curr_hist2%idx = curr_hist2%idx + 1
          sim1%t = curr_hist1%t_vals(curr_hist1%idx)
          sim2%t = curr_hist2%t_vals(curr_hist2%idx)
          call update_bounds_from_trace(curr_hist1, trace_length)
          call update_bounds_from_trace(curr_hist2, trace_length)

        case ('a', 'A')
          if (curr_hist1%idx > 1) then
            curr_hist1%idx = curr_hist1%idx - 1
            curr_hist2%idx = curr_hist2%idx - 1
            call load_state_from_history(curr_hist1, sim1)
            call load_state_from_history(curr_hist2, sim2)
            call update_bounds_from_trace(curr_hist1, trace_length)
            call update_bounds_from_trace(curr_hist2, trace_length)
          end if
        
        case ('w', 'W', 's', 'S')
          if (ch == 'w' .or. ch == 'W') then
            sim1%tau = sim1%tau + 0.01
            sim2%tau = sim2%tau + 0.01
          else
            sim1%tau = max(0.001, sim1%tau - 0.01)
            sim2%tau = max(0.001, sim2%tau - 0.01)
          end if
          curr_hist1%size = curr_hist1%idx
          curr_hist2%size = curr_hist2%idx
        case default
          cycle 
      end select
    end do

    call pgclos(ier)
    deallocate(curr_hist1%pos(1)%x, curr_hist1%pos(1)%y, curr_hist1%pos(2)%x, curr_hist1%pos(2)%y)
    deallocate(curr_hist2%pos(1)%x, curr_hist2%pos(1)%y, curr_hist2%pos(2)%x, curr_hist2%pos(2)%y)
  end subroutine simulate_interactive

  real function get_real(msg)
    character(len=*), intent(in) :: msg
    write(*,'(A,1X)',advance='no') trim(msg)
    read*, get_real
  end function get_real

end module lab_functions

program lab_5
  use lab_functions
  implicit none
  type(system_state) :: sim1, sim2
  integer, parameter :: out_unit = 12
  real, dimension(2) :: v1, v2
  real :: N, T1_theory, T2_theory
  real :: R1, R2, v_rel1_sq, v_rel2_sq, eps1, eps2, a1, a2

  ! input data
  do
    N = get_real('N:')
    if (N <= 0) then
      write(0,'(A)') "[err] Unsupported N, it should be positive."
    else
      exit
    end if
  end do
  do
    sim1%b1%m = get_real('m1:')
    if (sim1%b1%m > 0) exit
    write(0,'(A)') "[err] Mass must be positive."
  end do
  sim2%b1%m = sim1%b1%m / N

  sim1%b1%r(1) = get_real('x01:')
  sim1%b1%r(2) = get_real('y01:')
  sim2%b1%r(1) = sim1%b1%r(1) / N
  sim2%b1%r(2) = sim1%b1%r(2) / N
  v1(1) = get_real('v1x:')
  v1(2) = get_real('v1y:')

  do
    sim1%b2%m = get_real('m2:')
    if (sim1%b2%m > 0) exit
    write(0,'(A)') "[err] Mass must be positive."
  end do
  sim2%b2%m = sim1%b2%m / N

  do
    sim1%b2%r(1) = get_real('x02:')
    sim1%b2%r(2) = get_real('y02:')
    if (abs(sim1%b1%r(1) - sim1%b2%r(1)) > eps .or. &
        abs(sim1%b1%r(2) - sim1%b2%r(2)) > eps) exit
    write(0,'(A)') "[err] Bodies cannot be at the same point."
  end do
  sim2%b2%r(1) = sim1%b2%r(1) / N
  sim2%b2%r(2) = sim1%b2%r(2) / N

  v2(1) = get_real('v2x:')
  v2(2) = get_real('v2y:')

  do
    sim1%tau = get_real('tau (time step):')
    if (sim1%tau <= 0) then
      write(0,'(A)') "[err] Unsupported time, it should be positive."
    else
      exit
    end if
  end do
  sim2%tau = sim1%tau

  sim1%tau_init = sim1%tau
  sim2%tau_init = sim2%tau
  sim1%t = 0.0
  sim2%t = 0.0

  call update_accelerations(sim1)
  call update_accelerations(sim2)
  sim1%b1%r_old = sim1%b1%r - sim1%tau * v1 + 0.5 * sim1%b1%a * sim1%tau ** 2
  sim1%b2%r_old = sim1%b2%r - sim1%tau * v2 + 0.5 * sim1%b2%a * sim1%tau ** 2

  sim2%b1%r_old = sim2%b1%r - sim2%tau * v1 / N + 0.5 * sim2%b1%a * sim2%tau ** 2
  sim2%b2%r_old = sim2%b2%r - sim2%tau * v2 / N + 0.5 * sim2%b2%a * sim2%tau ** 2
  
  sim1%b1_init = sim1%b1
  sim1%b2_init = sim1%b2

  sim2%b1_init = sim2%b1
  sim2%b2_init = sim2%b2

  ! Система 1
  R1 = sqrt(sum((sim1%b1%r - sim1%b2%r)**2))
  v_rel1_sq = sum((v1 - v2)**2)
  eps1 = v_rel1_sq / 2.0 - G * (sim1%b1%m + sim1%b2%m) / R1
  a1 = -G * (sim1%b1%m + sim1%b2%m) / (2.0 * eps1)
  T1_theory = 2.0 * PI * sqrt(a1**3 / (G * (sim1%b1%m + sim1%b2%m)))

  ! Система 2
  R2 = R1 / N
  v_rel2_sq = v_rel1_sq / (N**2)
  eps2 = v_rel2_sq / 2.0 - G * (sim2%b1%m + sim2%b2%m) / R2
  a2 = -G * (sim2%b1%m + sim2%b2%m) / (2.0 * eps2)
  T2_theory = 2.0 * PI * sqrt(a2**3 / (G * (sim2%b1%m + sim2%b2%m)))

  write(*,*) "--- Theoretical calculation ---"
  write(*,*) "T1:", T1_theory
  write(*,*) "T2:", T2_theory
  write(*,*) "Ratio T1/T2:", T1_theory / T2_theory

  call simulate_interactive(sim1, sim2, 100)
end program lab_5