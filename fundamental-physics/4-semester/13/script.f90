module cinema_params
  implicit none
  integer, parameter :: MAX_TRIALS = 100000
end module cinema_params

module cinema_logic
  use cinema_params
  implicit none

  contains

  function simulate_seating(n) result(success)
    integer, intent(in) :: n
    logical :: success
    logical, allocatable :: seats(:)
    integer :: i, j, vasya_choice, count_free, target_idx, current_free
    real :: r
    allocate(seats(n))
    seats = .true.
    call random_number(r)
    vasya_choice = int(r * n) + 1
    seats(vasya_choice) = .false.
    do i = 2, n - 1
      if (seats(i)) then
        seats(i) = .false.
      else
        count_free = 0
        do j = 1, n
          if (seats(j)) then
            count_free = count_free + 1
          end if
        end do
        call random_number(r)
        target_idx = int(r * count_free) + 1
        current_free = 0
        do j = 1, n
          if (seats(j)) then
            current_free = current_free + 1
            if (current_free == target_idx) then
              seats(j) = .false.
              exit
            end if
          end if
        end do
      end if
    end do
    success = seats(n)
    deallocate(seats)
  end function simulate_seating

  subroutine draw_convergence(current_step, history, n_seats, step_size)
    integer, intent(in) :: current_step, n_seats, step_size
    real, intent(in) :: history(MAX_TRIALS)
    real, allocatable :: x_axis(:), y_axis(:)
    integer :: i
    character(len=100) :: title, info
    real :: x_max

    if (current_step < 1) then
        call pgpage()
        call pgvstd()
        call pgswin(0.0, 10.0, 0.0, 1.0)
        call pgsci(1)
        call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
        call pglab('Trials', 'Probability', 'Press D to start')
        return
    end if

    allocate(x_axis(current_step), y_axis(current_step))
    do i = 1, current_step 
        x_axis(i) = real(i) 
        y_axis(i) = history(i)
    end do

    x_max = real(current_step)
    if (x_max < 10.0) x_max = 10.0

    call pgpage()
    call pgvstd()
    call pgswin(0.0, x_max, 0.0, 1.0)
    
    call pgsci(1) ! Black
    call pgbox('BCNST', 0.0, 0, 'BCNST', 0.0, 0)
    
    write(title, '("N=", I0, " | Step Size: ", I0, " | Trial: ", I0)') n_seats, step_size, current_step
    call pglab('Trials (Adaptive)', 'Probability', title)

    call pgsci(2) ! Red
    call pgmove(0.0, 0.5)
    call pgdraw(x_max, 0.5)

    call pgsci(4) ! Blue
    call pgline(current_step, x_axis, y_axis)

    write(info, '("P = ", F6.4)') history(current_step)
    call pgsci(1)
    call pgtext(x_max * 0.05, 0.9, info)

    deallocate(x_axis, y_axis)
  end subroutine draw_convergence
end module cinema_logic

program cinema_adaptive
  use cinema_params
  use cinema_logic
  implicit none

  integer :: n_seats, total_success, current_step, step_size, i
  real :: history(MAX_TRIALS)
  integer :: pgopen
  real :: px, py
  character(len=1) :: key
  logical :: quit

  call random_seed()

  write(*,*) "Interactive simulation"
  write(*,*) "Controls:"
  write(*,*) "- D - next trial"
  write(*,*) "- W - increase step size by 10"
  write(*,*) "- S - decrease step size by 10"
  write(*,*) "- R - reset"
  write(*,*) "- Q - quit"
  write(*,*) "Enter N:"
  read(*,*) n_seats

  if (pgopen('/XSERVE') <= 0) stop
  call pgask(.false.)
  call pgscr(0, 1.0, 1.0, 1.0) 
  call pgscr(1, 0.0, 0.0, 0.0)

  quit = .false.
  
  10 continue
  total_success = 0
  current_step = 0
  history = 0.0
  step_size = 1

  do while (.not. quit)
    call draw_convergence(current_step, history, n_seats, step_size)
    call pgcurs(px, py, key)
    
    select case (key)
    case ('d', 'D')
      do i = 1, step_size
        if (current_step < MAX_TRIALS) then
          current_step = current_step + 1
          if (simulate_seating(n_seats)) total_success = total_success + 1
          history(current_step) = real(total_success) / real(current_step)
        end if
      end do
    case ('w', 'W')
      step_size = min(step_size + 10, 500)
    case ('s', 'S')
      step_size = max(1, step_size - 10)
    case ('r', 'R')
      goto 10
    case ('q', 'Q')
      quit = .true.
    end select
  end do

  call pgend()
end program cinema_adaptive