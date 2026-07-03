module lab_types
  implicit none

  type :: body
    real :: m
    real, dimension(2) :: r, r_old, a
  end type body

  type :: coord_pointer
    real, pointer :: x(:) => null(), y(:) => null()
    real, pointer :: ax(:) => null(), ay(:) => null()
    real, pointer :: ox(:) => null(), oy(:) => null()
  end type coord_pointer

  type :: history
    type(coord_pointer) :: pos(2)
    real, pointer :: t_vals(:) => null()
    real :: min_x, min_y, max_x, max_y
    integer :: size, idx, t_count, current_step_num
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
  real, parameter :: EPS = 1e-5
  
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

  subroutine verlet_back(state, historical_tau)
    type(system_state), intent(inout) :: state
    real, intent(in) :: historical_tau
    real, dimension(2) :: dist_vec, prev_r1, prev_r2
    real :: r_dist, force

    dist_vec = state%b2%r_old - state%b1%r_old
    r_dist = sqrt(sum(dist_vec**2))
    if (r_dist < 0.01) r_dist = 0.01
    
    force = G * state%b1%m * state%b2%m / (r_dist**2)
    state%b1%a = (force / state%b1%m) * (dist_vec / r_dist)
    state%b2%a = (force / state%b2%m) * (-dist_vec / r_dist)

    prev_r1 = 2.0 * state%b1%r_old - state%b1%r + state%b1%a * historical_tau**2
    prev_r2 = 2.0 * state%b2%r_old - state%b2%r + state%b2%a * historical_tau**2

    write(0,*) state%b1%r_old, prev_r1

    state%b1%r = state%b1%r_old
    state%b1%r_old = prev_r1
    
    state%b2%r = state%b2%r_old
    state%b2%r_old = prev_r2
  end subroutine verlet_back

  subroutine shift_left(hist, trace_length)
    type(history), intent(inout) :: hist
    integer, intent(in) :: trace_length
    integer :: i
    do i = 1, 2
      hist%pos(i)%x(1:trace_length-1)  = hist%pos(i)%x(2:trace_length)
      hist%pos(i)%y(1:trace_length-1)  = hist%pos(i)%y(2:trace_length)
      hist%pos(i)%ax(1:trace_length-1) = hist%pos(i)%ax(2:trace_length)
      hist%pos(i)%ay(1:trace_length-1) = hist%pos(i)%ay(2:trace_length)
      hist%pos(i)%ox(1:trace_length-1) = hist%pos(i)%ox(2:trace_length)
      hist%pos(i)%oy(1:trace_length-1) = hist%pos(i)%oy(2:trace_length)
    end do
  end subroutine shift_left

  subroutine shift_right(hist, trace_length)
    type(history), intent(inout) :: hist
    integer, intent(in) :: trace_length
    integer :: i
    do i = 1, 2
      hist%pos(i)%x(2:trace_length)  = hist%pos(i)%x(1:trace_length-1)
      hist%pos(i)%y(2:trace_length)  = hist%pos(i)%y(1:trace_length-1)
      hist%pos(i)%ax(2:trace_length) = hist%pos(i)%ax(1:trace_length-1)
      hist%pos(i)%ay(2:trace_length) = hist%pos(i)%ay(1:trace_length-1)
      hist%pos(i)%ox(2:trace_length) = hist%pos(i)%ox(1:trace_length-1)
      hist%pos(i)%oy(2:trace_length) = hist%pos(i)%oy(1:trace_length-1)
    end do
  end subroutine shift_right

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

  subroutine load_state_at_idx(hist, state, target_idx)
    type(history), intent(in) :: hist
    type(system_state), intent(inout) :: state
    integer, intent(in) :: target_idx
    integer :: b

    do b = 1, 2
      state%b1%r(1)     = merge(hist%pos(1)%x(target_idx), state%b1%r(1), b==1)
      state%b1%r(2)     = merge(hist%pos(1)%y(target_idx), state%b1%r(2), b==1)
      state%b1%a(1)     = merge(hist%pos(1)%ax(target_idx), state%b1%a(1), b==1)
      state%b1%a(2)     = merge(hist%pos(1)%ay(target_idx), state%b1%a(2), b==1)
      state%b1%r_old(1) = merge(hist%pos(1)%ox(target_idx), state%b1%r_old(1), b==1)
      state%b1%r_old(2) = merge(hist%pos(1)%oy(target_idx), state%b1%r_old(2), b==1)
    end do
    state%t = hist%t_vals(target_idx)
  end subroutine load_state_at_idx

  subroutine load_state_from_history(hist, state)
    type(history), intent(in) :: hist
    type(system_state), intent(inout) :: state
    integer :: i
    i = hist%idx
    
    state%b1%r(1)     = hist%pos(1)%x(i)
    state%b1%r(2)     = hist%pos(1)%y(i)
    state%b1%a(1)     = hist%pos(1)%ax(i)
    state%b1%a(2)     = hist%pos(1)%ay(i)
    state%b1%r_old(1) = hist%pos(1)%ox(i)
    state%b1%r_old(2) = hist%pos(1)%oy(i)
    
    state%b2%r(1)     = hist%pos(2)%x(i)
    state%b2%r(2)     = hist%pos(2)%y(i)
    state%b2%a(1)     = hist%pos(2)%ax(i)
    state%b2%a(2)     = hist%pos(2)%ay(i)
    state%b2%r_old(1) = hist%pos(2)%ox(i)
    state%b2%r_old(2) = hist%pos(2)%oy(i)
    
    state%t = hist%t_vals(hist%current_step_num)
  end subroutine load_state_from_history

  subroutine reset_simulation(sim, hist)
    type(system_state), intent(inout) :: sim
    type(history), intent(inout) :: hist

    sim%b1 = sim%b1_init
    sim%b2 = sim%b2_init
    sim%t = 0.0
    sim%tau = sim%tau_init

    hist%size = 1 
    hist%idx = 1
    hist%current_step_num = 1
    
    hist%t_count = 0 
    
    call save_to_idx(hist, sim, 1)

    call record_time(hist, sim%t)
    
    hist%min_x = min(sim%b1%r(1), sim%b2%r(1))
    hist%max_x = max(sim%b1%r(1), sim%b2%r(1))
    hist%min_y = min(sim%b1%r(2), sim%b2%r(2))
    hist%max_y = max(sim%b1%r(2), sim%b2%r(2))
  end subroutine reset_simulation

  subroutine save_to_idx(hist, state, target_idx)
    type(history), intent(inout) :: hist
    type(system_state), intent(in) :: state
    integer, intent(in) :: target_idx
    integer :: b
    
    do b = 1, 2
      hist%pos(b)%x(target_idx)  = merge(state%b1%r(1), state%b2%r(1), b==1)
      hist%pos(b)%y(target_idx)  = merge(state%b1%r(2), state%b2%r(2), b==1)
      hist%pos(b)%ax(target_idx) = merge(state%b1%a(1), state%b2%a(1), b==1)
      hist%pos(b)%ay(target_idx) = merge(state%b1%a(2), state%b2%a(2), b==1)
      hist%pos(b)%ox(target_idx) = merge(state%b1%r_old(1), state%b2%r_old(1), b==1)
      hist%pos(b)%oy(target_idx) = merge(state%b1%r_old(2), state%b2%r_old(2), b==1)
    end do
  end subroutine save_to_idx

  subroutine record_time(hist, t)
    type(history), intent(inout) :: hist
    real, intent(in) :: t
    real, pointer :: tmp(:)
    
    hist%t_count = hist%t_count + 1
    if (hist%t_count > size(hist%t_vals)) then
      allocate(tmp(size(hist%t_vals)*2))
      tmp(1:size(hist%t_vals)) = hist%t_vals
      deallocate(hist%t_vals)
      hist%t_vals => tmp
    end if
    hist%t_vals(hist%t_count) = t
  end subroutine record_time

  subroutine simulate_interactive(sim, trace_length)
    type(system_state), intent(inout) :: sim
    type(system_state) :: st_tmp
    integer, intent(in) :: trace_length
    integer :: pgopen, ier, left_bound_trace, n_points
    real :: unused
    character(len=1) :: ch
    character(len=20) :: t_str, tau_str
    type(history) :: curr_hist
    
    allocate(curr_hist%pos(1)%x(trace_length),&
             curr_hist%pos(1)%y(trace_length),&
             curr_hist%pos(1)%ax(trace_length),&
             curr_hist%pos(1)%ay(trace_length),&
             curr_hist%pos(1)%ox(trace_length),&
             curr_hist%pos(1)%oy(trace_length),&
             curr_hist%pos(2)%x(trace_length),&
             curr_hist%pos(2)%y(trace_length),&
             curr_hist%pos(2)%ax(trace_length),&
             curr_hist%pos(2)%ay(trace_length),&
             curr_hist%pos(2)%ox(trace_length),&
             curr_hist%pos(2)%oy(trace_length))
    
    allocate(curr_hist%t_vals(trace_length))

    call reset_simulation(sim, curr_hist)

    ier = pgopen('/XSERVE')
    if (ier .ne. 1) stop
    call pgask(.false.)
    call pgscr(0, 1.0, 1.0, 1.0) ! white background
    call pgscr(1, 0.0, 0.0, 0.0) ! black pen

    do
      call pgbbuf()
      call pgeras()
      call pgsci(1)
      call pgenv(curr_hist%min_x - 1.0, curr_hist%max_x + 1.0, curr_hist%min_y - 1.0, curr_hist%max_y + 1.0, 1, 0)
      write(t_str, '(A, F7.2, A)') 'T = ', sim%t, 's'
      call pgmtxt('B', 2.0, 0.0, 0.5, t_str)
      write(tau_str, '(A, F7.3, A)') 'tau = ', sim%tau, 's'
      call pgmtxt('B', 2.0, 1.0, 0.5, tau_str)
      call pglab('X', 'Y', 'D: Forward | A: Back | R: Reset | Q: Quit')

      ! draw trajectory
      if (curr_hist%idx > 1 .and. trace_length > 0) then
        call pgsls(2); call pgsci(15)
        
        left_bound_trace = max(1, curr_hist%idx - trace_length + 1)
        n_points = curr_hist%idx - left_bound_trace + 1
        
        call pgline(n_points,&
                    curr_hist%pos(1)%x(left_bound_trace:curr_hist%idx),&
                    curr_hist%pos(1)%y(left_bound_trace:curr_hist%idx))
        call pgline(n_points,&
                    curr_hist%pos(2)%x(left_bound_trace:curr_hist%idx),&
                    curr_hist%pos(2)%y(left_bound_trace:curr_hist%idx))
      end if

      call pgsls(1)
      call pgsci(2); call pgpt(1, curr_hist%pos(1)%x(curr_hist%idx), curr_hist%pos(1)%y(curr_hist%idx), 17)
      call pgsci(4); call pgpt(1, curr_hist%pos(2)%x(curr_hist%idx), curr_hist%pos(2)%y(curr_hist%idx), 17)

      call pgband(0, 0, unused, unused, unused, unused, ch)

      select case (ch)
        case ('q', 'Q')
          exit
        
        case ('r', 'R')
          call reset_simulation(sim, curr_hist)
          
        case ('d', 'D')
          if (curr_hist%idx == curr_hist%size) then
            if (curr_hist%current_step_num == curr_hist%t_count) then
              call verlet_step(sim)
              sim%t = sim%t + sim%tau
              call record_time(curr_hist, sim%t)
            else
              call verlet_step(sim)
              sim%t = curr_hist%t_vals(curr_hist%current_step_num + 1)
            end if

            curr_hist%current_step_num = curr_hist%current_step_num + 1

            if (curr_hist%size < trace_length) then
              curr_hist%size = curr_hist%size + 1
              curr_hist%idx = curr_hist%size
            else
              call shift_left(curr_hist, trace_length)
              curr_hist%idx = trace_length
            end if
            call save_to_idx(curr_hist, sim, curr_hist%idx)
          else
            curr_hist%idx = curr_hist%idx + 1
            curr_hist%current_step_num = curr_hist%current_step_num + 1
            call load_state_from_history(curr_hist, sim)
          end if
          call update_bounds_from_trace(curr_hist, trace_length)

        case ('a', 'A')
          if (curr_hist%current_step_num > trace_length) then
            st_tmp%b1%r(1) = curr_hist%pos(1)%x(2)
            st_tmp%b1%r(2) = curr_hist%pos(1)%y(2)
            st_tmp%b2%r(1) = curr_hist%pos(2)%x(2)
            st_tmp%b2%r(2) = curr_hist%pos(2)%y(2)

            st_tmp%b1%r_old(1) = curr_hist%pos(1)%x(1)
            st_tmp%b1%r_old(2) = curr_hist%pos(1)%y(1)
            st_tmp%b2%r_old(1) = curr_hist%pos(2)%x(1)
            st_tmp%b2%r_old(2) = curr_hist%pos(2)%y(1)

            st_tmp%b1%m = sim%b1%m
            st_tmp%b2%m = sim%b2%m
            
            call verlet_back(st_tmp, curr_hist%t_vals(curr_hist%current_step_num - trace_length))
            call shift_right(curr_hist, trace_length)
            call save_to_idx(curr_hist, st_tmp, 1)
            curr_hist%current_step_num = curr_hist%current_step_num - 1
            write(0,*) curr_hist%current_step_num, curr_hist%pos(1)%x(1), curr_hist%pos(1)%ox(1), st_tmp%b1%r(1), st_tmp%b1%r_old(1)
          else
            if (curr_hist%size > 1) then
              curr_hist%size = curr_hist%size - 1
              curr_hist%idx = curr_hist%size
              curr_hist%current_step_num = curr_hist%current_step_num - 1
            end if
          end if
          call load_state_from_history(curr_hist, sim)
          call update_bounds_from_trace(curr_hist, trace_length)
        
        case ('w', 'W', 's', 'S')
          if (ch == 'w' .or. ch == 'W') then
            sim%tau = sim%tau + 0.01
          else
            sim%tau = max(0.001, sim%tau - 0.01)
          end if
          curr_hist%size = curr_hist%idx
        case default
          cycle 
      end select
    end do

    call pgclos(ier)
    deallocate(curr_hist%pos(1)%x, curr_hist%pos(1)%y, curr_hist%pos(2)%x, curr_hist%pos(2)%y)
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
  type(system_state) :: sim
  integer, parameter :: out_unit = 12
  real, dimension(2) :: v1, v2

  ! input data
  do
    sim%b1%m = get_real('m1:')
    if (sim%b1%m > 0) exit
    write(0,'(A)') "[err] Mass must be positive."
  end do
  sim%b1%r(1) = get_real('x01:')
  sim%b1%r(2) = get_real('y01:')
  v1(1) = get_real('v1x:')
  v1(2) = get_real('v1y:')

  do
    sim%b2%m = get_real('m2:')
    if (sim%b2%m > 0) exit
    write(0,'(A)') "[err] Mass must be positive."
  end do
  do
    sim%b2%r(1) = get_real('x02:')
    sim%b2%r(2) = get_real('y02:')
    if (abs(sim%b1%r(1) - sim%b2%r(1)) > EPS .or. &
        abs(sim%b1%r(2) - sim%b2%r(2)) > EPS) exit
    write(0,'(A)') "[err] Bodies cannot be at the same point."
  end do
  v2(1) = get_real('v2x:')
  v2(2) = get_real('v2y:')

  do
    sim%tau = get_real('tau (time step):')
    if (sim%tau <= 0) then
      write(0,'(A)') "[err] Unsupported time, it should positive."
    else
      exit
    end if
  end do
  sim%tau_init = sim%tau
  sim%t = 0.0

  call update_accelerations(sim)
  sim%b1%r_old = sim%b1%r - sim%tau * v1 + 0.5 * sim%b1%a * sim%tau ** 2
  sim%b2%r_old = sim%b2%r - sim%tau * v2 + 0.5 * sim%b2%a * sim%tau ** 2
  
  sim%b1_init = sim%b1
  sim%b2_init = sim%b2

  call simulate_interactive(sim, 100)
end program lab_5