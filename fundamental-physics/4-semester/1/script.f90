function f(v)
  real :: f, v
  f = 10 - 0.004 * v ** 2
end function

function get_real(msg)
  real :: get_real
  character(len=*), intent(in) :: msg
  write(0,'(A, 1X)',advance='no') trim(msg)
  read*, get_real
end function

program lab_1
  real :: v = 0, s = 0, t = 0, h, threshold, t_r, k_1, k_2, k_3, k_4
  h = get_real('Set h (step):')
  threshold = get_real('Set desired s (in metres):')
  t_r = get_real('Right bound for time:')
  do
    t = t + h
    if (t > t_r) then
      exit
    end if
    k_1 = f(v)
    k_2 = f(v + h * k_1 / 2)
    k_3 = f(v + h * k_2 / 2)
    k_4 = f(v + h * k_3)
    v = v + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6
    s = s + v * h
    if (s >= threshold) then
      write(0,'(A, 1X)',advance='no') 'Estimated time:'
      write(0,'(f0.6)',advance='no') t
      print*, 'seconds'
      stop 0
    end if
  end do
  write(0,'(A, 1X)',advance='no') "Can't reach"
  write(0,'(f0.2, 1X)',advance='no') threshold
  write(0,'(A, 1X)',advance='no') 'metres in'
  write(0,'(f0.2)',advance='no') t_r
  print*,'seconds'
  stop 1
end program lab_1