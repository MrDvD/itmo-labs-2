package lib

type DotParams struct {
	X string  `json:"X"`
	Y float64 `json:"Y"`
	R string  `json:"R"`
}

type DotStatus struct {
	Entry    DotParams `json:"entry"`
	Hit      bool      `json:"hit"`
	Date     string    `json:"date"`
	Duration string    `json:"duration"`
}
