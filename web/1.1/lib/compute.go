package lib

import (
	"math"
	"strconv"
	"time"
)

func doesDotHit(dot DotParams) (bool, error) {
	X, err := strconv.Atoi(dot.X)
	if err != nil {
		return false, err
	}
	R, err := strconv.ParseFloat(dot.R, 32)
	if err != nil {
		return false, err
	}
	if X <= 0 && dot.Y >= 0 && dot.Y <= math.Sqrt(R*R-float64(X*X)) {
		return true, nil
	}
	if X >= 0 && float64(X) <= R && dot.Y >= -R/2 {
		return dot.Y <= (R-float64(X))/2, nil
	}
	return false, nil
}

func wrapDotStatus(dot DotParams) (DotStatus, error) {
	var dotStatus DotStatus
	var err error
	startTime := time.Now()
	dotStatus.Date = startTime.Format("2006-01-02 15:04:05")
	dotStatus.Entry = dot
	dotStatus.Hit, err = doesDotHit(dot)
	endTime := time.Now()
	dotStatus.Duration = endTime.Sub(startTime).String()
	return dotStatus, err
}
