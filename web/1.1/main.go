package main

import (
	"fmt"
	"mrdvd/lib"
	"net/http"
)

func main() {
	host := "localhost:8080"
	s := &http.Server{
		Addr:    host,
		Handler: http.HandlerFunc(lib.Serve),
	}
	fmt.Printf("Starting server at %s\n", host)
	err := s.ListenAndServe()
	if err != nil {
		fmt.Println("Error starting the server:", err)
	}
}
